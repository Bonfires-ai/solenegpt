/**
 * x402 protocol — exact-scheme types for Solana (SVM).
 *
 * Spec: https://github.com/coinbase/x402/blob/main/specs/schemes/exact/scheme_exact_svm.md
 */

export const X402_VERSION = 2;
export const SCHEME_EXACT = 'exact' as const;

// CAIP-2 network identifiers (the value after "solana:" is the genesis-hash chunk).
export const NETWORK_SOLANA_MAINNET = 'solana:5eykt4UsFv8P8NJdTREpY1vzqKqZKvdp';
export const NETWORK_SOLANA_DEVNET = 'solana:EtWTRABZaYq6iMfeYKouRu166VU2xqa1';

// USDC SPL mint addresses.
export const USDC_MAINNET_MINT = 'EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v';
export const USDC_DEVNET_MINT = '4zMMC9srt5Ri5X14GAgXhaHii3GnPAEERYPJgZJDncDU';

export const USDC_DECIMALS = 6;

export interface PaymentRequirements {
  scheme: typeof SCHEME_EXACT;
  network: string;
  amount: string; // smallest units (string to allow big numbers)
  asset: string; // SPL token mint
  payTo: string; // base58 receiver pubkey
  maxTimeoutSeconds: number;
  extra: {
    feePayer: string; // base58 facilitator pubkey
    memo?: string;
  };
}

export interface PaymentResource {
  url: string;
  description: string;
  mimeType: string;
}

/** Body of the 402 response from a Resource Server. */
export interface PaymentRequiredBody {
  x402Version: number;
  resource: PaymentResource;
  accepts: PaymentRequirements[];
}

/** What sits inside the (base64) X-PAYMENT header. */
export interface PaymentPayload {
  x402Version: number;
  resource: PaymentResource;
  accepted: PaymentRequirements;
  payload: {
    /** base64-encoded, serialized, partially-signed VersionedTransaction */
    transaction: string;
  };
}

export interface VerifyResult {
  isValid: boolean;
  invalidReason?: string;
}

export interface SettleResult {
  success: boolean;
  transaction: string; // base58 tx signature
  network: string;
  payer: string;
  error?: string;
}
