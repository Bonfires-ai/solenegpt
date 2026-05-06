import { PaymentPayload } from './spec';

/** Encode a PaymentPayload as the value of the X-PAYMENT HTTP header. */
export function encodeXPaymentHeader(payload: PaymentPayload): string {
  const json = JSON.stringify(payload);
  if (typeof window !== 'undefined') {
    return btoa(unescape(encodeURIComponent(json)));
  }
  return Buffer.from(json, 'utf-8').toString('base64');
}

/** Decode an X-PAYMENT header value into a PaymentPayload. */
export function decodeXPaymentHeader(header: string): PaymentPayload {
  if (typeof window !== 'undefined') {
    const json = decodeURIComponent(escape(atob(header)));
    return JSON.parse(json) as PaymentPayload;
  }
  const json = Buffer.from(header, 'base64').toString('utf-8');
  return JSON.parse(json) as PaymentPayload;
}
