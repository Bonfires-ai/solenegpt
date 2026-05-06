import { createFacilitator } from '@/lib/facilitator';
import { decodeXPaymentHeader } from '@/lib/x402/header';
import {
  NETWORK_SOLANA_DEVNET,
  NETWORK_SOLANA_MAINNET,
  type PaymentRequirements,
  type PaymentResource,
  SCHEME_EXACT,
  USDC_DECIMALS,
  USDC_DEVNET_MINT,
  USDC_MAINNET_MINT,
  X402_VERSION,
} from '@/lib/x402/spec';
import { SignJWT } from 'jose';
import { NextRequest, NextResponse } from 'next/server';
import { randomUUID } from 'node:crypto';

export const dynamic = 'force-dynamic';
export const revalidate = 0;

const SESSION_TTL_SECONDS = 600;

function buildRequirements(feePayer: string): PaymentRequirements {
  const isMainnet = (process.env.NEXT_PUBLIC_SOLANA_NETWORK ?? 'devnet').toLowerCase() === 'mainnet';
  const usdAmount = parseFloat(process.env.NEXT_PUBLIC_PAYMENT_DEFAULT_AMOUNT ?? '0.01');
  const amountSmallestUnits = String(Math.round(usdAmount * 10 ** USDC_DECIMALS));
  return {
    scheme: SCHEME_EXACT,
    network: isMainnet ? NETWORK_SOLANA_MAINNET : NETWORK_SOLANA_DEVNET,
    amount: amountSmallestUnits,
    asset: isMainnet ? USDC_MAINNET_MINT : USDC_DEVNET_MINT,
    payTo: process.env.SOLANA_RECIPIENT_ADDRESS as string,
    maxTimeoutSeconds: 60,
    extra: { feePayer },
  };
}

export async function POST(req: NextRequest) {
  const jwtSecret = process.env.VOICE_SESSION_JWT_SECRET;
  if (!jwtSecret) {
    return NextResponse.json({ error: 'VOICE_SESSION_JWT_SECRET not configured' }, { status: 500 });
  }
  if (!process.env.SOLANA_RECIPIENT_ADDRESS) {
    return NextResponse.json({ error: 'SOLANA_RECIPIENT_ADDRESS not configured' }, { status: 500 });
  }

  let facilitator;
  try {
    facilitator = createFacilitator();
  } catch (err) {
    return NextResponse.json(
      { error: err instanceof Error ? err.message : 'facilitator config error' },
      { status: 500 }
    );
  }

  let feePayer: string;
  try {
    feePayer = await facilitator.getFeePayer();
  } catch (err) {
    return NextResponse.json(
      { error: err instanceof Error ? err.message : 'facilitator unreachable' },
      { status: 502 }
    );
  }

  const requirements = buildRequirements(feePayer);
  const xPayment = req.headers.get('x-payment');

  if (!xPayment) {
    const resource: PaymentResource = {
      url: new URL(req.url).toString(),
      description: 'Voice mentoring session with Solène',
      mimeType: 'application/json',
    };
    return NextResponse.json({ x402Version: X402_VERSION, resource, accepts: [requirements] }, { status: 402 });
  }

  let payload;
  try {
    payload = decodeXPaymentHeader(xPayment);
  } catch {
    return NextResponse.json({ error: 'Invalid X-PAYMENT header' }, { status: 400 });
  }

  const verifyResult = await facilitator.verify(payload, requirements);
  if (!verifyResult.isValid) {
    return NextResponse.json({ error: verifyResult.invalidReason ?? 'Verification failed' }, { status: 402 });
  }

  const settleResult = await facilitator.settle(payload, requirements);
  if (!settleResult.success) {
    return NextResponse.json({ error: settleResult.error ?? 'Settlement failed' }, { status: 502 });
  }

  const secret = new TextEncoder().encode(jwtSecret);
  const sessionToken = await new SignJWT({ session_type: 'voice' })
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
