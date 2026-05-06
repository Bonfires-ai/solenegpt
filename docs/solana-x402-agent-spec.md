# Solana x402 Implementation Spec (for coding agents)

> **Audience:** A coding agent (Claude Code, Cursor, Aider, etc.) implementing Solana x402 payments in an existing Next.js 14 (App Router) project.
>
> **Companion doc:** [solana-x402-guide.md](./solana-x402-guide.md) — read that first if you need the *why*. This doc is the *what* and the *how*, optimized for execution.

---

## 0. Mission

Add a Solana USDC x402 payment gate to an HTTP endpoint in a Next.js app. The endpoint must:

1. Return HTTP `402` with x402 v2 payment requirements when called without payment.
2. Accept an `X-PAYMENT` header carrying a partially-signed Solana `VersionedTransaction`.
3. Verify the payment off-chain, then have a facilitator co-sign as fee payer and broadcast the tx on Solana.
4. On success, mint a single-use, time-limited JWT session token and return it.

The implementation MUST support both a **self-hosted facilitator** (default) and **Coinbase CDP** behind one interface, switchable via env var.

---

## 1. Stack assumptions

If the target project doesn't match these, STOP and ask the user before proceeding:

- **Next.js**: `^14.2` with App Router (`app/` directory)
- **React**: `^18.3`
- **TypeScript**: `^5.x`
- **Node**: `>= 20`
- **Package manager**: `pnpm` (npm/yarn work but commands shown use pnpm)
- **Browser wallet**: user has Phantom or another Solana Wallet Standard wallet

---

## 2. Package installation

Run exactly:

```bash
pnpm add \
  @solana/web3.js@^1.95 \
  @solana/spl-token@^0.4 \
  @solana/wallet-adapter-base@^0.9 \
  @solana/wallet-adapter-react@^0.15 \
  @solana/wallet-adapter-react-ui@^0.9 \
  @tanstack/react-query@^5 \
  bs58@^6 \
  jose@^6
```

> **DO NOT** install `@solana/wallet-adapter-wallets`. It is a meta-package that pulls in 30+ legacy adapters with React 16 peer deps and breaks Next.js client bootstrap. Phantom/Solflare/Backpack auto-register via the Solana Wallet Standard.

---

## 3. File inventory (create in this order)

| # | Path | Purpose | Depends on |
|---|---|---|---|
| 1 | `lib/x402/spec.ts` | Protocol types, network IDs, token mints | — |
| 2 | `lib/x402/header.ts` | Base64 codec for `X-PAYMENT` header | spec |
| 3 | `lib/facilitator/types.ts` | `FacilitatorClient` interface | spec |
| 4 | `lib/facilitator/selfhosted.ts` | In-process verifier + settler | types, spec |
| 5 | `lib/facilitator/coinbase.ts` | Coinbase CDP client | types, spec |
| 6 | `lib/facilitator/index.ts` | Factory keyed off env var | selfhosted, coinbase |
| 7 | `lib/x402/payment-builder.ts` | Client-side: build + sign tx | spec |
| 8 | `context/SolanaWalletContext.tsx` | Wallet adapter provider | — |
| 9 | `hooks/useX402Payment.ts` | Client-side payment state machine | header, payment-builder, spec |
| 10 | `app/api/paid/<your-resource>/route.ts` | The gated endpoint | facilitator, header, spec |
| 11 | `app/layout.tsx` | Wrap app in `SolanaWalletContextProvider` | context |
| 12 | `scripts/x402-setup.mjs` | One-shot keypair + secret generator | — |

After creating each file, run `pnpm tsc --noEmit` to confirm types check before moving on.

---

## 4. File contents

### 4.1 `lib/x402/spec.ts`

```ts
export const X402_VERSION = 2;
export const SCHEME_EXACT = 'exact' as const;

// CAIP-2 network IDs
export const NETWORK_SOLANA_MAINNET = 'solana:5eykt4UsFv8P8NJdTREpY1vzqKqZKvdp';
export const NETWORK_SOLANA_DEVNET = 'solana:EtWTRABZaYq6iMfeYKouRu166VU2xqa1';

// USDC SPL mints
export const USDC_MAINNET_MINT = 'EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v';
export const USDC_DEVNET_MINT = '4zMMC9srt5Ri5X14GAgXhaHii3GnPAEERYPJgZJDncDU'; // Circle's official devnet mint
export const USDC_DECIMALS = 6;

export interface PaymentRequirements {
  scheme: typeof SCHEME_EXACT;
  network: string;
  amount: string;       // smallest units, string for big numbers
  asset: string;        // SPL token mint
  payTo: string;        // base58 recipient pubkey
  maxTimeoutSeconds: number;
  extra: { feePayer: string; memo?: string };
}

export interface PaymentResource {
  url: string;
  description: string;
  mimeType: string;
}

export interface PaymentRequiredBody {
  x402Version: number;
  resource: PaymentResource;
  accepts: PaymentRequirements[];
}

export interface PaymentPayload {
  x402Version: number;
  resource: PaymentResource;
  accepted: PaymentRequirements;
  payload: { transaction: string }; // base64 VersionedTransaction
}

export interface VerifyResult {
  isValid: boolean;
  invalidReason?: string;
}

export interface SettleResult {
  success: boolean;
  transaction: string;  // base58 tx signature
  network: string;
  payer: string;
  error?: string;
}
```

### 4.2 `lib/x402/header.ts`

```ts
import { PaymentPayload } from './spec';

export function encodeXPaymentHeader(payload: PaymentPayload): string {
  const json = JSON.stringify(payload);
  if (typeof window !== 'undefined') {
    return btoa(unescape(encodeURIComponent(json)));
  }
  return Buffer.from(json, 'utf-8').toString('base64');
}

export function decodeXPaymentHeader(header: string): PaymentPayload {
  if (typeof window !== 'undefined') {
    const json = decodeURIComponent(escape(atob(header)));
    return JSON.parse(json) as PaymentPayload;
  }
  const json = Buffer.from(header, 'base64').toString('utf-8');
  return JSON.parse(json) as PaymentPayload;
}
```

### 4.3 `lib/facilitator/types.ts`

```ts
import { PaymentPayload, PaymentRequirements, SettleResult, VerifyResult } from '../x402/spec';

export interface FacilitatorClient {
  verify(payment: PaymentPayload, requirements: PaymentRequirements): Promise<VerifyResult>;
  settle(payment: PaymentPayload, requirements: PaymentRequirements): Promise<SettleResult>;
  getFeePayer(): Promise<string>;
}
```

### 4.4 `lib/facilitator/selfhosted.ts`

```ts
import { Connection, Keypair, PublicKey, VersionedTransaction } from '@solana/web3.js';
import { TOKEN_PROGRAM_ID, TOKEN_2022_PROGRAM_ID, getAssociatedTokenAddressSync } from '@solana/spl-token';
import bs58 from 'bs58';
import { FacilitatorClient } from './types';
import { PaymentPayload, PaymentRequirements, SettleResult, VerifyResult } from '../x402/spec';

export class SelfHostedFacilitator implements FacilitatorClient {
  private readonly connection: Connection;
  private readonly facilitatorKey: Keypair;

  constructor(rpcUrl: string, facilitatorSecretBase58: string) {
    this.connection = new Connection(rpcUrl, 'confirmed');
    this.facilitatorKey = Keypair.fromSecretKey(bs58.decode(facilitatorSecretBase58));
  }

  async getFeePayer(): Promise<string> {
    return this.facilitatorKey.publicKey.toBase58();
  }

  async verify(payment: PaymentPayload, req: PaymentRequirements): Promise<VerifyResult> {
    try {
      const tx = VersionedTransaction.deserialize(Buffer.from(payment.payload.transaction, 'base64'));
      const accountKeys = tx.message.staticAccountKeys;
      if (accountKeys.length === 0) return { isValid: false, invalidReason: 'no account keys' };

      const feePayer = accountKeys[0].toBase58();
      if (feePayer !== this.facilitatorKey.publicKey.toBase58()) {
        return { isValid: false, invalidReason: `feePayer ${feePayer} != facilitator` };
      }
      if (feePayer !== req.extra.feePayer) {
        return { isValid: false, invalidReason: 'feePayer in tx != requirements' };
      }

      // CRITICAL: scan ALL ix for TransferChecked. Wallets (Phantom) inject
      // their own ComputeBudget ix on sign, shifting our ix away from index 2.
      const compiledIxs = tx.message.compiledInstructions;
      const transferIxIdx = compiledIxs.findIndex((ix) => {
        const programId = accountKeys[ix.programIdIndex];
        if (!programId.equals(TOKEN_PROGRAM_ID) && !programId.equals(TOKEN_2022_PROGRAM_ID)) return false;
        const data = Buffer.from(ix.data);
        return data.length >= 10 && data[0] === 12; // discriminator 12 = TransferChecked
      });
      if (transferIxIdx === -1) return { isValid: false, invalidReason: 'no TransferChecked' };

      const transferIx = compiledIxs[transferIxIdx];
      const data = Buffer.from(transferIx.data);

      const amountInTx = data.readBigUInt64LE(1);
      if (amountInTx !== BigInt(req.amount)) {
        return { isValid: false, invalidReason: `amount ${amountInTx} != ${req.amount}` };
      }

      const ixKeys = transferIx.accountKeyIndexes;
      if (ixKeys.length < 4) return { isValid: false, invalidReason: 'TransferChecked needs 4 accounts' };

      const mint = accountKeys[ixKeys[1]];
      const destAta = accountKeys[ixKeys[2]];
      if (mint.toBase58() !== req.asset) {
        return { isValid: false, invalidReason: `mint ${mint.toBase58()} != ${req.asset}` };
      }

      const expectedDestAta = getAssociatedTokenAddressSync(
        new PublicKey(req.asset),
        new PublicKey(req.payTo),
      ).toBase58();
      if (destAta.toBase58() !== expectedDestAta) {
        return { isValid: false, invalidReason: `destAta ${destAta.toBase58()} != ${expectedDestAta}` };
      }

      return { isValid: true };
    } catch (err) {
      return { isValid: false, invalidReason: err instanceof Error ? err.message : 'verify failed' };
    }
  }

  async settle(payment: PaymentPayload, req: PaymentRequirements): Promise<SettleResult> {
    try {
      const tx = VersionedTransaction.deserialize(Buffer.from(payment.payload.transaction, 'base64'));
      tx.sign([this.facilitatorKey]);
      const sig = await this.connection.sendRawTransaction(tx.serialize(), { skipPreflight: false });
      await this.connection.confirmTransaction(sig, 'confirmed');
      return {
        success: true,
        transaction: sig,
        network: req.network,
        payer: this.facilitatorKey.publicKey.toBase58(),
      };
    } catch (err) {
      return {
        success: false,
        transaction: '',
        network: req.network,
        payer: this.facilitatorKey.publicKey.toBase58(),
        error: err instanceof Error ? err.message : 'settle failed',
      };
    }
  }
}
```

### 4.5 `lib/facilitator/coinbase.ts`

```ts
import { SignJWT, importPKCS8 } from 'jose';
import { FacilitatorClient } from './types';
import { PaymentPayload, PaymentRequirements, SettleResult, VerifyResult } from '../x402/spec';

interface CoinbaseFacilitatorOptions {
  apiKeyId: string;
  apiKeySecret: string;  // PEM-formatted EC private key
  url?: string;
}

const DEFAULT_URL = 'https://api.cdp.coinbase.com/platform/v2/x402';

export class CoinbaseFacilitator implements FacilitatorClient {
  private readonly apiKeyId: string;
  private readonly apiKeySecret: string;
  private readonly url: string;
  private feePayerCache?: { value: string; expiresAt: number };

  constructor({ apiKeyId, apiKeySecret, url }: CoinbaseFacilitatorOptions) {
    this.apiKeyId = apiKeyId;
    this.apiKeySecret = apiKeySecret;
    this.url = url ?? DEFAULT_URL;
  }

  async getFeePayer(): Promise<string> {
    const now = Date.now();
    if (this.feePayerCache && this.feePayerCache.expiresAt > now) return this.feePayerCache.value;
    const data = await this.request<{ feePayer: string }>('GET', '/supported');
    if (!data.feePayer) throw new Error('Coinbase facilitator: no feePayer in /supported response');
    this.feePayerCache = { value: data.feePayer, expiresAt: now + 60_000 };
    return data.feePayer;
  }

  async verify(payment: PaymentPayload, requirements: PaymentRequirements): Promise<VerifyResult> {
    return this.request<VerifyResult>('POST', '/verify', { paymentPayload: payment, paymentRequirements: requirements });
  }

  async settle(payment: PaymentPayload, requirements: PaymentRequirements): Promise<SettleResult> {
    return this.request<SettleResult>('POST', '/settle', { paymentPayload: payment, paymentRequirements: requirements });
  }

  private async request<T>(method: 'GET' | 'POST', path: string, body?: unknown): Promise<T> {
    const fullUrl = this.url.replace(/\/$/, '') + path;
    const auth = await this.signJwt(method, new URL(fullUrl));
    const res = await fetch(fullUrl, {
      method,
      headers: { Authorization: `Bearer ${auth}`, 'Content-Type': 'application/json' },
      body: body ? JSON.stringify(body) : undefined,
    });
    if (!res.ok) throw new Error(`Coinbase ${method} ${path} ${res.status}: ${await res.text().catch(() => '')}`);
    return (await res.json()) as T;
  }

  private async signJwt(method: string, url: URL): Promise<string> {
    const key = await importPKCS8(this.apiKeySecret, 'ES256');
    const now = Math.floor(Date.now() / 1000);
    return new SignJWT({
      iss: 'cdp',
      aud: ['cdp_service'],
      uri: `${method} ${url.host}${url.pathname}`,
    })
      .setProtectedHeader({ alg: 'ES256', kid: this.apiKeyId, typ: 'JWT' })
      .setSubject(this.apiKeyId)
      .setIssuedAt(now)
      .setNotBefore(now)
      .setExpirationTime(now + 120)
      .sign(key);
  }
}
```

### 4.6 `lib/facilitator/index.ts`

```ts
import { CoinbaseFacilitator } from './coinbase';
import { SelfHostedFacilitator } from './selfhosted';
import { FacilitatorClient } from './types';

export type { FacilitatorClient } from './types';

let cached: FacilitatorClient | null = null;

export function createFacilitator(): FacilitatorClient {
  if (cached) return cached;
  const which = (process.env.X402_FACILITATOR ?? 'self').toLowerCase();
  switch (which) {
    case 'coinbase':
      cached = new CoinbaseFacilitator({
        apiKeyId: mustEnv('CDP_API_KEY_ID'),
        apiKeySecret: mustEnv('CDP_API_KEY_SECRET'),
        url: process.env.CDP_FACILITATOR_URL,
      });
      return cached;
    case 'self':
      cached = new SelfHostedFacilitator(mustEnv('SOLANA_RPC_URL'), mustEnv('FACILITATOR_KEYPAIR_SECRET'));
      return cached;
    default:
      throw new Error(`Unknown X402_FACILITATOR: "${which}"`);
  }
}

function mustEnv(key: string): string {
  const v = process.env[key];
  if (!v) throw new Error(`Missing env var: ${key}`);
  return v;
}
```

### 4.7 `lib/x402/payment-builder.ts`

```ts
import {
  ComputeBudgetProgram, Connection, PublicKey,
  TransactionMessage, VersionedTransaction,
} from '@solana/web3.js';
import {
  TOKEN_PROGRAM_ID,
  createAssociatedTokenAccountIdempotentInstruction,
  createTransferCheckedInstruction,
  getAssociatedTokenAddressSync,
} from '@solana/spl-token';
import type { WalletContextState } from '@solana/wallet-adapter-react';
import { PaymentRequirements, USDC_DECIMALS } from './spec';

export interface BuildPaymentArgs {
  connection: Connection;
  wallet: WalletContextState;
  requirements: PaymentRequirements;
}

export async function buildAndSignPayment({ connection, wallet, requirements }: BuildPaymentArgs): Promise<string> {
  if (!wallet.publicKey) throw new Error('Wallet not connected');
  if (!wallet.signTransaction) throw new Error('Wallet does not support signTransaction');

  const userPubkey = wallet.publicKey;
  const feePayer = new PublicKey(requirements.extra.feePayer);
  const recipient = new PublicKey(requirements.payTo);
  const mint = new PublicKey(requirements.asset);
  const amount = BigInt(requirements.amount);

  const sourceAta = getAssociatedTokenAddressSync(mint, userPubkey);
  const destAta = getAssociatedTokenAddressSync(mint, recipient);

  const cuLimitIx = ComputeBudgetProgram.setComputeUnitLimit({ units: 200_000 });
  const ensureDestAtaIx = createAssociatedTokenAccountIdempotentInstruction(
    feePayer, destAta, recipient, mint, TOKEN_PROGRAM_ID,
  );
  const transferIx = createTransferCheckedInstruction(
    sourceAta, mint, destAta, userPubkey,
    amount, USDC_DECIMALS, [], TOKEN_PROGRAM_ID,
  );

  const { blockhash } = await connection.getLatestBlockhash('finalized');
  const message = new TransactionMessage({
    payerKey: feePayer,
    recentBlockhash: blockhash,
    instructions: [cuLimitIx, ensureDestAtaIx, transferIx],
  }).compileToV0Message();

  const tx = new VersionedTransaction(message);
  const signed = await wallet.signTransaction(tx);
  return Buffer.from(signed.serialize()).toString('base64');
}
```

### 4.8 `context/SolanaWalletContext.tsx`

```tsx
'use client';

import { ConnectionProvider, WalletProvider } from '@solana/wallet-adapter-react';
import { WalletModalProvider } from '@solana/wallet-adapter-react-ui';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { type ReactNode, useMemo } from 'react';
import '@solana/wallet-adapter-react-ui/styles.css';

const queryClient = new QueryClient();
const WALLETS: never[] = []; // Wallet Standard auto-detects Phantom/Solflare/Backpack

export default function SolanaWalletContextProvider({ children }: { children: ReactNode }) {
  const endpoint = process.env.NEXT_PUBLIC_SOLANA_RPC_URL ?? 'https://api.devnet.solana.com';
  const wallets = useMemo(() => WALLETS, []);
  return (
    <ConnectionProvider endpoint={endpoint}>
      <WalletProvider wallets={wallets} autoConnect>
        <WalletModalProvider>
          <QueryClientProvider client={queryClient}>{children}</QueryClientProvider>
        </WalletModalProvider>
      </WalletProvider>
    </ConnectionProvider>
  );
}
```

### 4.9 `hooks/useX402Payment.ts`

```ts
'use client';

import { useConnection, useWallet } from '@solana/wallet-adapter-react';
import { useWalletModal } from '@solana/wallet-adapter-react-ui';
import { useCallback, useState } from 'react';
import { encodeXPaymentHeader } from '@/lib/x402/header';
import { buildAndSignPayment } from '@/lib/x402/payment-builder';
import type { PaymentRequiredBody, PaymentRequirements } from '@/lib/x402/spec';
import { X402_VERSION } from '@/lib/x402/spec';

export type X402Step =
  | 'DISCONNECTED' | 'WALLET_CONNECTED' | 'SIGNING'
  | 'PAYMENT_PENDING' | 'READY' | 'ERROR';

export interface UseX402PaymentArgs {
  endpoint: string;  // e.g. '/api/paid/your-resource'
}

export function useX402Payment({ endpoint }: UseX402PaymentArgs) {
  const { connection } = useConnection();
  const wallet = useWallet();
  const { setVisible } = useWalletModal();

  const [step, setStep] = useState<X402Step>('DISCONNECTED');
  const [error, setError] = useState<string | null>(null);
  const [response, setResponse] = useState<unknown>(null);
  const [txHash, setTxHash] = useState<string | null>(null);

  const isConnected = Boolean(wallet.connected && wallet.publicKey);

  const connectWallet = useCallback(() => {
    if (isConnected) { setStep('WALLET_CONNECTED'); return; }
    setVisible(true);
  }, [isConnected, setVisible]);

  const pay = useCallback(async () => {
    if (!wallet.publicKey) { setError('Connect wallet first'); return; }
    try {
      setError(null);
      setStep('SIGNING');

      const probe = await fetch(endpoint, { method: 'POST' });
      if (probe.status !== 402) {
        if (probe.ok) { setResponse(await probe.json()); setStep('READY'); return; }
        throw new Error(`Unexpected ${probe.status}`);
      }

      const body = (await probe.json()) as PaymentRequiredBody;
      const requirements: PaymentRequirements | undefined = body.accepts?.[0];
      if (!requirements) throw new Error('No requirements in 402');

      const transaction = await buildAndSignPayment({ connection, wallet, requirements });
      const xPayment = encodeXPaymentHeader({
        x402Version: X402_VERSION,
        resource: body.resource,
        accepted: requirements,
        payload: { transaction },
      });

      setStep('PAYMENT_PENDING');
      const paid = await fetch(endpoint, { method: 'POST', headers: { 'X-PAYMENT': xPayment } });
      if (!paid.ok) {
        const err = await paid.json().catch(() => ({}));
        throw new Error((err as { error?: string }).error ?? `Payment failed (${paid.status})`);
      }
      const data = await paid.json();
      setResponse(data);
      setTxHash(data.tx_hash ?? null);
      setStep('READY');
    } catch (err) {
      const msg = err instanceof Error ? err.message : 'Payment failed';
      if (msg.toLowerCase().includes('rejected') || msg.toLowerCase().includes('user denied')) {
        setStep('WALLET_CONNECTED'); setError(null);
      } else {
        setStep('ERROR'); setError(msg);
      }
    }
  }, [connection, wallet, endpoint]);

  return { step, error, response, txHash, isConnected, connectWallet, pay };
}
```

### 4.10 `app/api/paid/<your-resource>/route.ts`

> **Replace `<your-resource>` with whatever the gated resource is** (e.g. `voice/session`, `summary`, `report`). Replace the JWT minting body with whatever you actually want to return.

```ts
import { SignJWT } from 'jose';
import { randomUUID } from 'node:crypto';
import { NextRequest, NextResponse } from 'next/server';
import { createFacilitator } from '@/lib/facilitator';
import { decodeXPaymentHeader } from '@/lib/x402/header';
import {
  NETWORK_SOLANA_DEVNET, NETWORK_SOLANA_MAINNET,
  type PaymentRequirements, type PaymentResource,
  SCHEME_EXACT, USDC_DECIMALS, USDC_DEVNET_MINT, USDC_MAINNET_MINT, X402_VERSION,
} from '@/lib/x402/spec';

export const dynamic = 'force-dynamic';
export const revalidate = 0;

const SESSION_TTL_SECONDS = 600;

function buildRequirements(feePayer: string): PaymentRequirements {
  const isMainnet = (process.env.NEXT_PUBLIC_SOLANA_NETWORK ?? 'devnet').toLowerCase() === 'mainnet';
  const usdAmount = parseFloat(process.env.NEXT_PUBLIC_PAYMENT_DEFAULT_AMOUNT ?? '0.01');
  return {
    scheme: SCHEME_EXACT,
    network: isMainnet ? NETWORK_SOLANA_MAINNET : NETWORK_SOLANA_DEVNET,
    amount: String(Math.round(usdAmount * 10 ** USDC_DECIMALS)),
    asset: isMainnet ? USDC_MAINNET_MINT : USDC_DEVNET_MINT,
    payTo: process.env.SOLANA_RECIPIENT_ADDRESS as string,
    maxTimeoutSeconds: 60,
    extra: { feePayer },
  };
}

export async function POST(req: NextRequest) {
  const jwtSecret = process.env.X402_SESSION_JWT_SECRET;
  if (!jwtSecret) return NextResponse.json({ error: 'X402_SESSION_JWT_SECRET unset' }, { status: 500 });
  if (!process.env.SOLANA_RECIPIENT_ADDRESS) return NextResponse.json({ error: 'SOLANA_RECIPIENT_ADDRESS unset' }, { status: 500 });

  let facilitator;
  try { facilitator = createFacilitator(); }
  catch (err) { return NextResponse.json({ error: err instanceof Error ? err.message : 'facilitator config' }, { status: 500 }); }

  let feePayer: string;
  try { feePayer = await facilitator.getFeePayer(); }
  catch (err) { return NextResponse.json({ error: err instanceof Error ? err.message : 'facilitator unreachable' }, { status: 502 }); }

  const requirements = buildRequirements(feePayer);
  const xPayment = req.headers.get('x-payment');

  if (!xPayment) {
    const resource: PaymentResource = {
      url: new URL(req.url).toString(),
      description: 'Replace with your resource description',
      mimeType: 'application/json',
    };
    return NextResponse.json({ x402Version: X402_VERSION, resource, accepts: [requirements] }, { status: 402 });
  }

  let payload;
  try { payload = decodeXPaymentHeader(xPayment); }
  catch { return NextResponse.json({ error: 'Invalid X-PAYMENT header' }, { status: 400 }); }

  const verifyResult = await facilitator.verify(payload, requirements);
  if (!verifyResult.isValid) return NextResponse.json({ error: verifyResult.invalidReason ?? 'Verify failed' }, { status: 402 });

  const settleResult = await facilitator.settle(payload, requirements);
  if (!settleResult.success) return NextResponse.json({ error: settleResult.error ?? 'Settle failed' }, { status: 502 });

  const secret = new TextEncoder().encode(jwtSecret);
  const sessionToken = await new SignJWT({ session_type: 'paid' })
    .setProtectedHeader({ alg: 'HS256' })
    .setSubject(randomUUID())
    .setJti(randomUUID())
    .setIssuedAt()
    .setExpirationTime(`${SESSION_TTL_SECONDS}s`)
    .sign(secret);

  return NextResponse.json({
    session_token: sessionToken,
    expires_in: SESSION_TTL_SECONDS,
    tx_hash: settleResult.transaction,
  });
}
```

### 4.11 `app/layout.tsx` (modification)

Wrap the existing `<body>` children with `SolanaWalletContextProvider`:

```tsx
import SolanaWalletContextProvider from '@/context/SolanaWalletContext';

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        <SolanaWalletContextProvider>{children}</SolanaWalletContextProvider>
      </body>
    </html>
  );
}
```

### 4.12 `scripts/x402-setup.mjs`

```js
#!/usr/bin/env node
import { Keypair } from '@solana/web3.js';
import bs58 from 'bs58';
import crypto from 'node:crypto';

const kp = Keypair.generate();
const secret = bs58.encode(kp.secretKey);
const pubkey = kp.publicKey.toBase58();
const jwt = crypto.randomBytes(48).toString('base64');

console.log('FACILITATOR_KEYPAIR_SECRET=' + secret);
console.log('X402_SESSION_JWT_SECRET=' + jwt);
console.log('Facilitator pubkey (fund with SOL):', pubkey);
```

---

## 5. Environment variables

Add to `.env.local`:

```bash
# Required
SOLANA_RPC_URL=https://api.devnet.solana.com
NEXT_PUBLIC_SOLANA_RPC_URL=https://api.devnet.solana.com
NEXT_PUBLIC_SOLANA_NETWORK=devnet
SOLANA_RECIPIENT_ADDRESS=<base58 wallet that receives USDC>
X402_SESSION_JWT_SECRET=<random 48 bytes, base64>
NEXT_PUBLIC_PAYMENT_DEFAULT_AMOUNT=0.01

# Self-hosted facilitator (default)
X402_FACILITATOR=self
FACILITATOR_KEYPAIR_SECRET=<base58 secret key, generate via scripts/x402-setup.mjs>

# Coinbase facilitator (only if X402_FACILITATOR=coinbase)
# CDP_API_KEY_ID=...
# CDP_API_KEY_SECRET=...
```

After setting `FACILITATOR_KEYPAIR_SECRET`, fund the facilitator pubkey with devnet SOL:

```bash
# May rate-limit; use https://faucet.solana.com if so
curl -X POST https://api.devnet.solana.com -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"requestAirdrop","params":["<facilitator-pubkey>",1000000000]}'
```

---

## 6. Smoke tests (run in order)

After each step, fix any failures before moving on.

### 6.1 TypeScript checks

```bash
pnpm tsc --noEmit
```

Expected: no errors.

### 6.2 Endpoint returns 402 without payment

```bash
curl -s -X POST http://localhost:3000/api/paid/<your-resource> -w "\nHTTP %{http_code}\n"
```

Expected: `HTTP 402` and a JSON body with `x402Version: 2`, `resource`, and `accepts: [...]`.

### 6.3 Endpoint returns 500 if env vars missing

Temporarily unset `X402_SESSION_JWT_SECRET`, restart, hit the endpoint:

Expected: `HTTP 500` with `{ "error": "X402_SESSION_JWT_SECRET unset" }`. Restore env after.

### 6.4 Facilitator pubkey query

```bash
curl -s -X POST $SOLANA_RPC_URL -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"getBalance","params":["<facilitator-pubkey>"]}'
```

Expected: `value` ≥ `1000000000` (1 SOL) once funded.

### 6.5 Browser smoke test

1. Open the page that hosts the payment UI.
2. Click "Connect Wallet" — Phantom modal appears.
3. Switch Phantom to Devnet (Settings → Developer Settings → Testnet Mode → Devnet).
4. Get USDC-Dev from [faucet.circle.com](https://faucet.circle.com/) for the buyer's wallet (mint must equal `USDC_DEVNET_MINT` in `spec.ts`).
5. Click "Pay" — Phantom prompts to sign the SPL transfer.
6. Approve.

Expected: `READY` step, response includes `session_token` and `tx_hash`. The tx is viewable on [explorer.solana.com](https://explorer.solana.com/?cluster=devnet) with the returned signature.

---

## 7. Anti-patterns (DO NOT)

| Don't | Reason |
|---|---|
| Don't install `@solana/wallet-adapter-wallets` | Drags in 30+ legacy adapters with React 16 peers; crashes Next.js hydration. Wallet Standard auto-detects modern wallets. |
| Don't hardcode `compiledInstructions[2]` for TransferChecked | Phantom prepends its own ComputeBudget ix on sign. **Always scan all ix** by program ID + discriminator. |
| Don't make the user's wallet the fee payer | Buyer would need SOL. Set `payerKey: feePayer` (facilitator) on the message; the facilitator co-signs in `settle`. |
| Don't omit `createAssociatedTokenAccountIdempotentInstruction` | First payment to a fresh recipient fails with "invalid account data" if the dest ATA doesn't exist. |
| Don't use `@solana/kit` (web3.js v2) | This spec assumes web3.js v1 APIs (`VersionedTransaction.deserialize`, `Connection`, etc.). v2 has a different shape. |
| Don't reuse the `X-PAYMENT` payload across requests | Each blockhash is short-lived and TransferChecked is single-use; replay attempts will fail at the chain anyway, but better to mint a new tx per request. |
| Don't put `FACILITATOR_KEYPAIR_SECRET` in `NEXT_PUBLIC_*` | Server-only secret. `NEXT_PUBLIC_*` ships to the browser. |
| Don't use `confirmTransaction(sig, 'finalized')` in self-hosted settle | `'confirmed'` (default) returns in ~400 ms; `'finalized'` waits ~13 s and will time out HTTP requests. |
| Don't trust the client's `requirements` in the `X-PAYMENT` payload | Server-side, always rebuild requirements from env on every request and verify the tx against THOSE, not what the client sent. |
| Don't skip `pnpm tsc --noEmit` between file creations | Catches typos and import errors before runtime. |

---

## 8. Definition of done

The task is complete when ALL of these are true:

- [ ] `pnpm tsc --noEmit` passes with zero errors
- [ ] `pnpm next build` passes with zero errors
- [ ] `curl -X POST /api/paid/<your-resource>` (no payment) returns HTTP 402 with valid x402 v2 JSON
- [ ] Browser flow: connect Phantom → pay → server returns `session_token` + `tx_hash`
- [ ] The returned `tx_hash` resolves on [explorer.solana.com?cluster=devnet](https://explorer.solana.com/?cluster=devnet) and shows a TransferChecked moving the configured USDC amount to the recipient's ATA
- [ ] Switching `X402_FACILITATOR=coinbase` (with valid CDP keys set) does NOT require any code changes
- [ ] No `@solana/wallet-adapter-wallets` import anywhere in the codebase
- [ ] `pnpm dev` boots without runtime errors in browser console

---

## 9. If something breaks

Look at the symptom in the table below. Each row is a real error we hit during initial implementation:

| Symptom | Cause | Fix |
|---|---|---|
| `Attempt to debit an account but found no record of a prior credit` | Facilitator has 0 SOL | Airdrop SOL to facilitator pubkey |
| `Error processing Instruction X: invalid account data for instruction` from Token program | User's source ATA doesn't exist (no USDC on this mint) OR mint mismatch | Faucet correct USDC mint to user; verify `asset` matches what faucet handed out |
| `instruction[N] is not an SPL token program instruction` (own verify code) | Hardcoded ix index instead of scanning | Use `findIndex` over compiled ix to locate TransferChecked by program ID + discriminator 12 |
| Hydration error / blank page | Imported `@solana/wallet-adapter-wallets` | Remove the import, pass `wallets={[]}` |
| `Wallet does not support signTransaction` | Wallet not connected, or non-Wallet-Standard wallet | Confirm `wallet.connected === true` before calling `pay()` |
| `Blockhash not found` on settle | Tx aged out between client-sign and server-broadcast | Use `getLatestBlockhash('finalized')` on client; settle promptly |
| `Cannot find matching keyid` on `pnpm install` | Stale corepack signing keys (Node 22.13 bug) | `COREPACK_INTEGRITY_KEYS=0 pnpm install` |
| `Coinbase facilitator GET /supported 401` | CDP API key invalid or JWT signing failed | Verify `CDP_API_KEY_SECRET` is the full PEM (`-----BEGIN EC PRIVATE KEY-----` ... `-----END EC PRIVATE KEY-----\n`) including line breaks |

---

## 10. Out of scope

This spec does NOT cover:

- Persisting JWT JTIs across restarts (in-memory dedup is fine for a single-instance dev server)
- Rate limiting (add at the edge — Vercel/Cloudflare/middleware)
- Refunds (x402 settlement is one-shot and final)
- Multi-recipient splits (you'd need a custom on-chain program)
- Mainnet deployment hardening (RPC failover, monitoring, key rotation)

These belong in a follow-up doc once the basic flow works.

---

## 11. Reference links

### x402 protocol
- Spec repo: https://github.com/coinbase/x402
- SVM (Solana) exact-scheme spec: https://github.com/coinbase/x402/blob/main/specs/schemes/exact/scheme_exact_svm.md
- Coinbase x402 docs: https://docs.cdp.coinbase.com/x402/welcome
- Coinbase x402 quickstart (sellers): https://docs.cdp.coinbase.com/x402/quickstart-for-sellers
- Coinbase x402 quickstart (buyers): https://docs.cdp.coinbase.com/x402/quickstart-for-buyers
- Solana x402 intro: https://solana.com/developers/guides/getstarted/intro-to-x402
- Build a Solana x402 facilitator (Solana Foundation): https://solana.com/developers/guides/getstarted/build-a-x402-facilitator
- Solana x402 reference template: https://solana.com/developers/templates/kit-node-solanax402

### SDKs (npm)
- `@x402/core`, `@x402/next`, `@x402/express`, `@x402/svm`, `@x402/fetch` — Coinbase official SDKs
- `x402-solana` — community SDK: https://www.npmjs.com/package/x402-solana
- `@payainetwork/x402-solana` — alternative community SDK
- `@rapid402/sdk` — Rapid402 client/server SDK

### Hosted facilitators
- Coinbase CDP portal (sign up for API keys): https://portal.cdp.coinbase.com/
- Coinbase facilitator base URL: `https://api.cdp.coinbase.com/platform/v2/x402`
- Rapid402: https://rapid402.com (verify uptime before betting on it)
- Coinbase pricing: 1,000 tx/month free, then $0.001/tx

### Solana RPC
- Devnet (free, rate-limited): `https://api.devnet.solana.com`
- Mainnet (free, heavy rate limits): `https://api.mainnet-beta.solana.com`
- Helius (paid mainnet, recommended for production): https://www.helius.dev/
- Triton One: https://triton.one
- QuickNode: https://www.quicknode.com/chains/sol

### Faucets
- Solana SOL devnet faucet (most reliable): https://faucet.solana.com/
- Helius devnet faucet: https://www.helius.dev/devnet-faucet
- QuickNode Solana faucet: https://faucet.quicknode.com
- Circle USDC devnet faucet (matches `USDC_DEVNET_MINT` constant): https://faucet.circle.com/
- spl-token-faucet (alt USDC-Dev mint, requires changing `asset`): https://spl-token-faucet.com/?token-name=USDC-Dev

### Wallets (browser; auto-register via Wallet Standard)
- Phantom: https://phantom.app/
- Solflare: https://solflare.com/
- Backpack: https://backpack.app/

### Wallet adapter
- Solana Wallet Adapter monorepo: https://github.com/anza-xyz/wallet-adapter
- `@solana/wallet-adapter-react`: https://www.npmjs.com/package/@solana/wallet-adapter-react
- `@solana/wallet-adapter-react-ui`: https://www.npmjs.com/package/@solana/wallet-adapter-react-ui
- Wallet Standard: https://github.com/wallet-standard/wallet-standard

### Solana libraries
- `@solana/web3.js` (v1.x — what this spec uses): https://solana-labs.github.io/solana-web3.js/v1.x/
- `@solana/spl-token`: https://www.npmjs.com/package/@solana/spl-token
- `@solana/kit` (formerly web3.js v2 — DO NOT use here, incompatible API): https://github.com/anza-xyz/kit

### CAIP-2 chain identifiers
- Solana CAIP-2 namespace: https://github.com/ChainAgnostic/namespaces/blob/main/solana/caip2.md
- Mainnet ID: `solana:5eykt4UsFv8P8NJdTREpY1vzqKqZKvdp`
- Devnet ID: `solana:EtWTRABZaYq6iMfeYKouRu166VU2xqa1`

### USDC mint addresses
- USDC mainnet (Circle): `EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v`
- USDC devnet (Circle, matches `faucet.circle.com`): `4zMMC9srt5Ri5X14GAgXhaHii3GnPAEERYPJgZJDncDU`
- USDC-Dev (spl-token-faucet variant, alt mint): `Gh9ZwEmdLJ8DscKNTkTqPbNwLNNBjuSzaG9Vp2KGtKJr`
- All USDC mints have **6 decimals**

### Block explorers (paste tx signatures or addresses)
- Solana Explorer: https://explorer.solana.com/ (set cluster dropdown to Devnet/Mainnet)
- Solscan: https://solscan.io
- SolanaFM: https://solana.fm

### Companion docs in this repo
- Human-oriented guide (concepts, pitfalls walkthrough): [solana-x402-guide.md](./solana-x402-guide.md)
- Reference implementation: see `lib/x402/`, `lib/facilitator/`, `app/api/paid/voice/session/` in this codebase
