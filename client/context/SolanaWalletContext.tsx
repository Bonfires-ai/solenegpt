'use client';

import { ConnectionProvider, WalletProvider } from '@solana/wallet-adapter-react';
import { WalletModalProvider } from '@solana/wallet-adapter-react-ui';
// Default wallet-adapter UI styling. Override via globals.css if you want.
import '@solana/wallet-adapter-react-ui/styles.css';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { type ReactNode, useMemo } from 'react';

const queryClient = new QueryClient();

// Phantom, Solflare, Backpack and other modern wallets implement the Solana
// Wallet Standard, so WalletProvider auto-detects them. We deliberately skip
// `@solana/wallet-adapter-wallets` — that meta-package drags in 30+ legacy
// adapters with React 16 peer deps that break Next.js client bootstrap.
const WALLETS: never[] = [];

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
