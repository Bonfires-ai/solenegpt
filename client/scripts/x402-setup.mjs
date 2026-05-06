#!/usr/bin/env node
/**
 * x402-setup.mjs — generate the secrets you need to wire up Solana x402.
 *
 * Run with: node scripts/x402-setup.mjs
 *
 * Outputs:
 *   - A fresh Solana keypair to act as the facilitator (signs tx fees)
 *   - A random JWT secret for minting voice session tokens
 *   - The pubkey + airdrop command so you can fund it on devnet
 *
 * Copy the printed env vars into .env.local. Run this only once.
 */
import { Keypair } from '@solana/web3.js';
import bs58 from 'bs58';
import crypto from 'node:crypto';

const kp = Keypair.generate();
const secretBase58 = bs58.encode(kp.secretKey);
const pubkey = kp.publicKey.toBase58();
const jwtSecret = crypto.randomBytes(48).toString('base64');

const line = '─'.repeat(72);
console.log(line);
console.log('  Solana x402 — generated values');
console.log(line);
console.log('');
console.log('  Add to client/.env.local:');
console.log('');
console.log(`    FACILITATOR_KEYPAIR_SECRET=${secretBase58}`);
console.log(`    VOICE_SESSION_JWT_SECRET=${jwtSecret}`);
console.log('');
console.log('  Facilitator pubkey (this is what sponsors tx fees):');
console.log('');
console.log(`    ${pubkey}`);
console.log('');
console.log('  Fund the facilitator with 1 devnet SOL:');
console.log('');
console.log(`    curl -X POST https://api.devnet.solana.com -H "Content-Type: application/json" \\`);
console.log(`      -d '{"jsonrpc":"2.0","id":1,"method":"requestAirdrop","params":["${pubkey}",1000000000]}'`);
console.log('');
console.log('  Or use the web faucet: https://faucet.solana.com/');
console.log('');
console.log(line);
console.log('  Next:');
console.log('    1. Set SOLANA_RECIPIENT_ADDRESS to YOUR Phantom wallet address');
console.log('    2. Get devnet USDC into your Phantom: https://spl-token-faucet.com/?token-name=USDC-Dev');
console.log('    3. Set NEXT_PUBLIC_PAYMENT_GATE=true');
console.log('    4. Restart the dev server');
console.log(line);
