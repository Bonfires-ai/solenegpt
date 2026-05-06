import { SignJWT, importPKCS8 } from 'jose';
import { PaymentPayload, PaymentRequirements, SettleResult, VerifyResult } from '../x402/spec';
import { FacilitatorClient } from './types';

interface CoinbaseFacilitatorOptions {
  apiKeyId: string;
  /** PEM-formatted ECDSA private key (BEGIN EC PRIVATE KEY block). */
  apiKeySecret: string;
  /** Defaults to https://api.cdp.coinbase.com/platform/v2/x402 */
  url?: string;
}

const DEFAULT_URL = 'https://api.cdp.coinbase.com/platform/v2/x402';

/**
 * Coinbase Developer Platform x402 facilitator client.
 *
 * Auth: per-request ECDSA-signed JWT in the Authorization header.
 * Their facilitator URL is fixed; you supply API key id + secret from
 * https://portal.cdp.coinbase.com/.
 *
 * NOTE: Coinbase has not published the verify/settle JSON shapes for v2 in
 * detail at the time of writing. We assume the request body is
 *   { paymentPayload, paymentRequirements }
 * and the response shape matches our VerifyResult / SettleResult. If their
 * API drifts, this file is the only place that needs to change.
 */
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
    if (this.feePayerCache && this.feePayerCache.expiresAt > now) {
      return this.feePayerCache.value;
    }
    const data = await this.request<{ feePayer: string }>('GET', '/supported');
    if (!data.feePayer) throw new Error('Coinbase facilitator did not return feePayer');
    this.feePayerCache = { value: data.feePayer, expiresAt: now + 60_000 };
    return data.feePayer;
  }

  async verify(payment: PaymentPayload, requirements: PaymentRequirements): Promise<VerifyResult> {
    return this.request<VerifyResult>('POST', '/verify', {
      paymentPayload: payment,
      paymentRequirements: requirements,
    });
  }

  async settle(payment: PaymentPayload, requirements: PaymentRequirements): Promise<SettleResult> {
    return this.request<SettleResult>('POST', '/settle', {
      paymentPayload: payment,
      paymentRequirements: requirements,
    });
  }

  private async request<T>(method: 'GET' | 'POST', path: string, body?: unknown): Promise<T> {
    const fullUrl = this.url.replace(/\/$/, '') + path;
    const auth = await this.signJwt(method, new URL(fullUrl));
    const res = await fetch(fullUrl, {
      method,
      headers: {
        Authorization: `Bearer ${auth}`,
        'Content-Type': 'application/json',
      },
      body: body ? JSON.stringify(body) : undefined,
    });
    if (!res.ok) {
      const text = await res.text().catch(() => '');
      throw new Error(`Coinbase facilitator ${method} ${path} ${res.status}: ${text}`);
    }
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
