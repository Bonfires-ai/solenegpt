import { PaymentPayload, PaymentRequirements, SettleResult, VerifyResult } from '../x402/spec';

/**
 * Vendor-agnostic interface for an x402 facilitator. Concrete implementations:
 *
 *   - SelfHostedFacilitator — runs in-process; signs+broadcasts via @solana/web3.js
 *   - CoinbaseFacilitator   — POSTs to api.cdp.coinbase.com/platform/v2/x402
 *
 * Pick one via the X402_FACILITATOR env var; see ./index.ts.
 */
export interface FacilitatorClient {
  /** Validate a payment payload without broadcasting. */
  verify(payment: PaymentPayload, requirements: PaymentRequirements): Promise<VerifyResult>;

  /** Co-sign as feePayer and broadcast to the network. */
  settle(payment: PaymentPayload, requirements: PaymentRequirements): Promise<SettleResult>;

  /**
   * Pubkey of the wallet that pays Solana network fees on every settled tx.
   * Goes into PaymentRequirements.extra.feePayer so the client can build the
   * partially-signed transaction with the correct payer.
   */
  getFeePayer(): Promise<string>;
}
