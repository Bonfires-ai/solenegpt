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
      throw new Error(`Unknown X402_FACILITATOR: "${which}" (expected "self" or "coinbase")`);
  }
}

function mustEnv(key: string): string {
  const v = process.env[key];
  if (!v) throw new Error(`Missing required env var: ${key}`);
  return v;
}
