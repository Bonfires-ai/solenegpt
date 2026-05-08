'use client';

/**
 * useVoiceSession — manages the paid voice session flow on Solana via x402.
 *
 * State machine:
 *   DISCONNECTED → WALLET_CONNECTED → SIGNING → PAYMENT_PENDING → SESSION_READY → IN_SESSION → ENDED
 *
 * Wire flow:
 *   1. Probe POST /api/paid/voice/session  → expect 402 + PaymentRequiredBody
 *   2. Build + sign USDC SPL transferChecked via wallet adapter
 *   3. Retry POST with X-PAYMENT header  → 200 + { session_token }
 *   4. Caller routes session_token to /api/connection-details
 */
import { encodeXPaymentHeader } from '@/lib/x402/header';
import { buildAndSignPayment } from '@/lib/x402/payment-builder';
import type { PaymentRequiredBody, PaymentRequirements } from '@/lib/x402/spec';
import { X402_VERSION } from '@/lib/x402/spec';
import { useConnection, useWallet } from '@solana/wallet-adapter-react';
import { useWalletModal } from '@solana/wallet-adapter-react-ui';
import { useCallback, useState } from 'react';

export type VoiceSessionStep =
  | 'DISCONNECTED'
  | 'WALLET_CONNECTED'
  | 'SIGNING'
  | 'PAYMENT_PENDING'
  | 'SESSION_READY'
  | 'IN_SESSION'
  | 'ENDED'
  | 'ERROR';

interface VoiceSessionResponse {
  session_token: string;
  expires_in: number;
  tx_hash?: string;
}

const PAID_ENDPOINT = '/api/paid/voice/session';
const PAYMENTS_DISABLED = process.env.NEXT_PUBLIC_DISABLE_X402 === 'true';

export interface UseVoiceSessionReturn {
  step: VoiceSessionStep;
  error: string | null;
  sessionToken: string | null;
  txHash: string | null;
  isConnected: boolean;
  paymentsDisabled: boolean;
  connectWallet: () => void;
  startPayment: () => Promise<void>;
  reset: () => void;
  isLoading: boolean;
}

export function useVoiceSession(): UseVoiceSessionReturn {
  const { connection } = useConnection();
  const wallet = useWallet();
  const { setVisible } = useWalletModal();

  const [step, setStep] = useState<VoiceSessionStep>(PAYMENTS_DISABLED ? 'WALLET_CONNECTED' : 'DISCONNECTED');
  const [error, setError] = useState<string | null>(null);
  const [sessionToken, setSessionToken] = useState<string | null>(null);
  const [txHash, setTxHash] = useState<string | null>(null);

  const isConnected = Boolean(wallet.connected && wallet.publicKey);

  const connectWallet = useCallback(() => {
    if (isConnected) {
      setStep('WALLET_CONNECTED');
      return;
    }
    setVisible(true);
  }, [isConnected, setVisible]);

  const startPayment = useCallback(async () => {
    if (!PAYMENTS_DISABLED && !wallet.publicKey) {
      setError('Connect your wallet first.');
      return;
    }

    try {
      setError(null);
      setStep('SIGNING');

      // 1. Probe — expect 402 with payment requirements
      const probe = await fetch(PAID_ENDPOINT, { method: 'POST' });

      if (probe.status !== 402) {
        if (probe.ok) {
          // Server accepted without payment (gate disabled). Still pull the token.
          const data = (await probe.json()) as VoiceSessionResponse;
          setSessionToken(data.session_token);
          setTxHash(data.tx_hash ?? null);
          setStep('SESSION_READY');
          return;
        }
        const body = await probe.json().catch(() => ({}));
        throw new Error(`Unexpected ${probe.status}: ${(body as { error?: string }).error ?? probe.statusText}`);
      }

      const body = (await probe.json()) as PaymentRequiredBody;
      const requirements: PaymentRequirements | undefined = body.accepts?.[0];
      if (!requirements) throw new Error('No payment requirements in 402 response');

      // 2. Build + sign the SPL transfer
      const transaction = await buildAndSignPayment({
        connection,
        wallet,
        requirements,
      });

      const xPayment = encodeXPaymentHeader({
        x402Version: X402_VERSION,
        resource: body.resource,
        accepted: requirements,
        payload: { transaction },
      });

      // 3. Retry with X-PAYMENT
      setStep('PAYMENT_PENDING');
      const paid = await fetch(PAID_ENDPOINT, {
        method: 'POST',
        headers: { 'X-PAYMENT': xPayment },
      });

      if (!paid.ok) {
        const errBody = await paid.json().catch(() => ({}));
        throw new Error((errBody as { error?: string }).error ?? `Payment failed (${paid.status})`);
      }

      const data = (await paid.json()) as VoiceSessionResponse;
      if (!data.session_token) throw new Error('No session token in response');

      setSessionToken(data.session_token);
      setTxHash(data.tx_hash ?? null);
      setStep('SESSION_READY');
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Payment failed';
      const userRejected =
        message.toLowerCase().includes('rejected') ||
        message.toLowerCase().includes('user denied') ||
        message.toLowerCase().includes('user cancelled');
      if (userRejected) {
        setStep('WALLET_CONNECTED');
        setError(null);
      } else {
        setStep('ERROR');
        setError(message);
      }
    }
  }, [connection, wallet]);

  const reset = useCallback(() => {
    setStep(PAYMENTS_DISABLED || isConnected ? 'WALLET_CONNECTED' : 'DISCONNECTED');
    setError(null);
    setSessionToken(null);
    setTxHash(null);
  }, [isConnected]);

  const isLoading = step === 'SIGNING' || step === 'PAYMENT_PENDING';

  return {
    step,
    error,
    sessionToken,
    txHash,
    isConnected,
    paymentsDisabled: PAYMENTS_DISABLED,
    connectWallet,
    startPayment,
    reset,
    isLoading,
  };
}
