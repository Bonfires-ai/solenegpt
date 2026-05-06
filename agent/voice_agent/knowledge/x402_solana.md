# What I know about x402 on Solana

x402 is HTTP's "402 Payment Required" status code, finally put to use. It lets any
HTTP endpoint demand a crypto payment before serving content. Stateless, no
sessions, no API keys — a server returns 402 with payment requirements, the
client signs, retries with an X-PAYMENT header, the server verifies and
serves.

I think Solana is the right home for x402:
- 400ms finality means the user isn't waiting awkwardly for confirmation
- Sub-cent fees make true micropayments viable — pay-per-call APIs work
- USDC SPL on Solana is the natural payment token

How the flow works on Solana:
- The client builds a partially-signed VersionedTransaction with a USDC
  TransferChecked instruction
- The facilitator's wallet is the fee payer — so the user doesn't need any SOL
- The user signs the transaction in their wallet (Phantom, Solflare, etc.)
- The signed tx is base64-encoded and sent in the X-PAYMENT header
- The server's facilitator co-signs as fee payer, broadcasts, and confirms
- Then mints whatever the actual access token is (a JWT, an API key, etc.)

The facilitator pattern is the elegant part. You can run your own (~150 lines
of TypeScript over @solana/web3.js) or use a hosted one like Coinbase's CDP
facilitator. Coinbase has a free tier of 1000 transactions per month, which
is generous for a hackathon project.

When I see builders working on x402, the pitfalls I've watched them hit:
- Hardcoding the TransferChecked instruction position. Phantom prepends its
  own ComputeBudget instruction on signing, so the verifier should scan for
  TransferChecked by program ID, not by index
- Mismatched USDC mint addresses — Circle's devnet USDC has its own address
  that's different from spl-token-faucet's USDC-Dev variant
- Forgetting to create the recipient's associated token account on first
  payment. Use createAssociatedTokenAccountIdempotent before the transfer
- Confusing the "facilitator fee payer" model — the user signs a tx where
  someone else's address is the payer. Phantom shows this correctly but it
  takes a moment to wrap your head around

For a real product, I'd recommend stablecoin payments on devnet first to test
the full handshake, then switch to mainnet by changing one env var. Use a
paid RPC like Helius for production — the public mainnet RPC will rate-limit
you under any real traffic.

This whole site uses x402 for the voice session. You pay 0.01 USDC, you get
10 minutes with me. Pretty cool.
