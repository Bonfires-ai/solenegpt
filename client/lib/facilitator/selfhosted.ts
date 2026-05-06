import { TOKEN_2022_PROGRAM_ID, TOKEN_PROGRAM_ID, getAssociatedTokenAddressSync } from '@solana/spl-token';
import { Connection, Keypair, PublicKey, VersionedTransaction } from '@solana/web3.js';
import bs58 from 'bs58';
import { PaymentPayload, PaymentRequirements, SettleResult, VerifyResult } from '../x402/spec';
import { FacilitatorClient } from './types';

/**
 * In-process x402 facilitator backed by a single Solana keypair.
 *
 * Operational requirements: the keypair must hold enough SOL to pay tx fees
 * for every settled payment (~0.000005 SOL per tx, free on devnet via faucet).
 *
 * Construction:
 *   new SelfHostedFacilitator(rpcUrl, base58SecretKey)
 */
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
      const txBytes = Buffer.from(payment.payload.transaction, 'base64');
      const tx = VersionedTransaction.deserialize(txBytes);

      const accountKeys = tx.message.staticAccountKeys;
      if (accountKeys.length === 0) {
        return { isValid: false, invalidReason: 'transaction has no account keys' };
      }

      const feePayer = accountKeys[0].toBase58();
      const expectedFeePayer = this.facilitatorKey.publicKey.toBase58();
      if (feePayer !== expectedFeePayer) {
        return { isValid: false, invalidReason: `feePayer ${feePayer} does not match facilitator ${expectedFeePayer}` };
      }
      if (feePayer !== req.extra.feePayer) {
        return { isValid: false, invalidReason: 'feePayer in transaction does not match payment requirements' };
      }

      // Spec says TransferChecked SHOULD be at index 2, but Phantom injects
      // its own priority-fee ComputeBudget ix on sign, which shifts ours.
      // Scan all compiled instructions for the TransferChecked (SPL token
      // program + discriminator 12) instead of hardcoding the position.
      const compiledIxs = tx.message.compiledInstructions;
      const transferIxIdx = compiledIxs.findIndex(ix => {
        const programId = accountKeys[ix.programIdIndex];
        const isSplToken = programId.equals(TOKEN_PROGRAM_ID) || programId.equals(TOKEN_2022_PROGRAM_ID);
        if (!isSplToken) return false;
        const data = Buffer.from(ix.data);
        return data.length >= 10 && data[0] === 12;
      });
      if (transferIxIdx === -1) {
        return { isValid: false, invalidReason: 'no TransferChecked instruction found in transaction' };
      }
      const transferIx = compiledIxs[transferIxIdx];
      const data = Buffer.from(transferIx.data);

      const amountInTx = data.readBigUInt64LE(1);
      const amountRequired = BigInt(req.amount);
      if (amountInTx !== amountRequired) {
        return { isValid: false, invalidReason: `amount ${amountInTx} does not match required ${amountRequired}` };
      }

      // TransferChecked accounts: [source, mint, destination, owner, ...]
      const ixKeys = transferIx.accountKeyIndexes;
      if (ixKeys.length < 4) {
        return { isValid: false, invalidReason: 'TransferChecked has fewer than 4 accounts' };
      }
      const mint = accountKeys[ixKeys[1]];
      const destAta = accountKeys[ixKeys[2]];

      if (mint.toBase58() !== req.asset) {
        return { isValid: false, invalidReason: `mint ${mint.toBase58()} does not match asset ${req.asset}` };
      }

      const expectedDestAta = getAssociatedTokenAddressSync(
        new PublicKey(req.asset),
        new PublicKey(req.payTo)
      ).toBase58();
      if (destAta.toBase58() !== expectedDestAta) {
        return {
          isValid: false,
          invalidReason: `destination ATA ${destAta.toBase58()} does not match payTo's ATA ${expectedDestAta}`,
        };
      }

      return { isValid: true };
    } catch (err) {
      return { isValid: false, invalidReason: err instanceof Error ? err.message : 'verify failed' };
    }
  }

  async settle(payment: PaymentPayload, req: PaymentRequirements): Promise<SettleResult> {
    try {
      const txBytes = Buffer.from(payment.payload.transaction, 'base64');
      const tx = VersionedTransaction.deserialize(txBytes);

      // Co-sign as feePayer; this fills the empty signature slot at index 0.
      tx.sign([this.facilitatorKey]);

      const rawTx = tx.serialize();
      const sig = await this.connection.sendRawTransaction(rawTx, { skipPreflight: false });

      // Poll-based confirmation (deprecated form, but still works and avoids
      // needing lastValidBlockHeight which is not on the deserialized tx).
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
