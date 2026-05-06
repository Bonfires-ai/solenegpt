import {
  TOKEN_PROGRAM_ID,
  createAssociatedTokenAccountIdempotentInstruction,
  createTransferCheckedInstruction,
  getAssociatedTokenAddressSync,
} from '@solana/spl-token';
import type { WalletContextState } from '@solana/wallet-adapter-react';
import { ComputeBudgetProgram, Connection, PublicKey, TransactionMessage, VersionedTransaction } from '@solana/web3.js';
import { PaymentRequirements, USDC_DECIMALS } from './spec';

export interface BuildPaymentArgs {
  connection: Connection;
  wallet: WalletContextState;
  requirements: PaymentRequirements;
}

/**
 * Build a partially-signed VersionedTransaction that pays `requirements.amount`
 * of `requirements.asset` from the connected wallet to `requirements.payTo`,
 * with `requirements.extra.feePayer` set as the transaction fee payer.
 *
 * Per x402 SVM spec, the third instruction (index 2) is the SPL TransferChecked.
 *
 * Returns the base64 string that goes into PaymentPayload.payload.transaction.
 */
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

  const transferIx = createTransferCheckedInstruction(
    sourceAta,
    mint,
    destAta,
    userPubkey,
    amount,
    USDC_DECIMALS,
    [],
    TOKEN_PROGRAM_ID
  );

  // Spec requires the SPL transfer to be at instruction index 2.
  // ix[0]: ComputeBudget unit limit (safe filler).
  // ix[1]: CreateATA-idempotent for the destination — no-op if it already
  //        exists, otherwise creates it (rent paid by feePayer = facilitator).
  //        This means a brand-new recipient address Just Works on first payment.
  // ix[2]: TransferChecked (mandatory per spec).
  const cuLimitIx = ComputeBudgetProgram.setComputeUnitLimit({ units: 200_000 });
  const ensureDestAtaIx = createAssociatedTokenAccountIdempotentInstruction(
    feePayer,
    destAta,
    recipient,
    mint,
    TOKEN_PROGRAM_ID
  );

  const { blockhash } = await connection.getLatestBlockhash('finalized');

  const message = new TransactionMessage({
    payerKey: feePayer,
    recentBlockhash: blockhash,
    instructions: [cuLimitIx, ensureDestAtaIx, transferIx],
  }).compileToV0Message();

  const tx = new VersionedTransaction(message);

  // User signs (partial signature — fee payer slot stays empty for the facilitator).
  const signed = await wallet.signTransaction(tx);

  const serialized = signed.serialize();
  return Buffer.from(serialized).toString('base64');
}
