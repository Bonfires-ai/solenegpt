# Dev3Pack Hackathon — AI Mentor Knowledge Base

> **Purpose of this document:** This is a structured knowledge base for an AI mentor agent supporting hackers during the Dev3Pack Solana Hackathon. It contains best practices, resources, and step-by-step guidance for participants from ideation to post-hackathon. Use it to answer questions, suggest next steps, and unblock builders.

---

## Mentor Agent Persona & Tone

- Be **direct, practical, and encouraging**. Hackers are time-constrained.
- Always tie advice back to **shipping a working app** (not a landing page).
- When a hacker is stuck, ask: *Where are you in the 5-step flow?* (Team & Ideation → Execution → Submission → Judging → After).
- Push hackers toward **meaningful, long-term projects** — not throwaway demos.
- Remind them: every app needs **users and liquidity**. If they can't explain who uses it and why, the idea isn't ready.

---

## The 5 Hackathon Steps (Master Flow)

1. **Find a team & Ideation**
2. **Execution**
3. **Submission**
4. **Judging**
5. **After hackathon**

The mentor should always know which step the hacker is in and tailor advice accordingly.

---

## Step 1 — Find a Team & Ideation

### 1.1 Available Tracks (Solana-related)

| Track | Difficulty | Notes |
|---|---|---|
| Solana app (open / "whatever") | Standard | Most flexible — any Solana dApp |
| Solana mobile | Standard | Build for Solana Mobile (Seeker / Saga ecosystem) |
| AI with ElevenLabs & Solana x402 | Standard | Voice AI + x402 payment protocol on Solana |
| DeFi on Solana with Li.Fi | Advanced | Cross-chain DeFi via Li.Fi integration |
| Robotics | Advanced | Hardware + Solana — most ambitious track |

### 1.2 Core Ideation Principles

These are the non-negotiables to repeat to every hacker:

- **All apps need users AND liquidity.** If the project has neither path, redesign it.
- **Build something meaningful to YOU.** Think about your personality and your region. Long-term focus beats short-term hype.
- **Mobile-friendly by default.** Think about your favorite *daily* app — that's the bar. If it's not something a person would open daily, rethink the hook.
- **Double-check the "why blockchain?" question.** If the project would work just as well as a Web2 app, it probably should be a Web2 app. The blockchain layer must add real value (ownership, composability, payments, censorship resistance, etc.).

### 1.3 Where to Find Ideas

- **Superteam Build — Ideas:** https://superteam.fun/build/ideas
- **SendAI Ideas (agentic projects):** https://ideas.sendai.fun/
- **Colosseum Copilot:** https://colosseum.com/copilot — pressure-test your idea against 5,400+ past hackathon submissions to see what's been done and where the gaps are.

### 1.4 Study Past Winners

Looking at winners is the fastest way to calibrate quality and scope:

- **Superteam past winners:** https://superteam.fun/build/past-hackathon-winners
- **Colosseum Agent Hackathon projects:** https://colosseum.com/agent-hackathon/projects
- **Solana Mobile winners** (linked in original deck)
- **Hackathon Projects (non-Solana, interesting crypto usage):** https://hackathonprojects.dev/

### 1.5 Benchmark Other Ecosystems

- Look at apps in other ecosystems (Ethereum, Base, Sui, etc.) and ask: *Does this exist on Solana yet? Could it work better here?*
- **Use DeFi Llama** (https://defillama.com) to check which ecosystem your category has liquidity in. If your app is DeFi-shaped, you need to land where the TVL already lives — or have a real plan to bootstrap it.

### 1.6 Get Mentor Feedback Early

- **Talk to mentors before writing code.** A 15-minute conversation can save 15 hours of building the wrong thing.
- Use **SoleneGPT** (https://solenegpt.bonfires.ai/) for AI-assisted feedback when human mentors aren't available.

---

## Step 2 — Execution

### 2.1 Get Started Checklist

In order:

1. **Set up a wallet and get fake (devnet) tokens.** Phantom is the recommended wallet.
2. **Lock in your idea** (don't keep changing it mid-build).
3. **Ask an AI to write a clear, detailed prompt** of what you want to build.
4. **Paste the prompt into NoahAI** (https://trynoah.ai) to scaffold the project.

### 2.2 Wallets & Devnet Setup

- **Phantom wallet:** https://phantom.com — primary recommended Solana wallet.
- **Solana Devnet Faucet:** Get free devnet SOL for testing — https://faucet.solana.com (airdrop SOL on devnet & testnet).
- **CRITICAL:** Use a **separate developer wallet** for the hackathon — never use a wallet that holds real funds. This is the single most common security mistake.

### 2.3 NoahAI (Free Credits for Dev3Pack)

- Fill in the **Noah AI x Dev3Pack Solana Hackathon form** to get free Noah credits.
- Sign up first at https://trynoah.ai and use the same registered email for the form.
- Follow @TryNoahAI on X and join the Noah Builders Telegram group (referenced in the form).

### 2.4 Solana Resources (Vibe Coding Checklist)

| Resource | URL | Use For |
|---|---|---|
| Solana Skills by SendAI | solanaskills.com | Agent skills directory |
| Agent Skills — Solana | solana.com/skills | Official Solana agent skills catalog |
| Solana Dev Skill | github.com/solana-foundation/solana-dev-skill | Official dev skill |
| solana.new | solana.new | 100+ in-built skills, MCPs, CLIs |
| NoahAI | trynoah.ai | Vibe-code A→Z your first Solana project |
| Awesome Solana AI | github.com/solana-foundation/awesome-solana-ai | Curated AI tools for Solana |

### 2.5 GitHub Setup

- **Create a repo and invite team members early** (not the night before submission).
- Make sure the repo is set up with a clean `main` branch and a `README.md` placeholder from day one.

### 2.6 What to Actually Build (Architecture)

A real submission almost always has these layers:

- **Web2 & Web3 login** (e.g., social login + wallet connect)
- **Smart contracts** (the on-chain logic)
- **Frontend** (the UI users actually touch)
- **Backend** — only if needed (don't add complexity for its own sake)

### 2.7 The #1 Execution Rule

> **Do NOT only build a landing page. Build a real, working app.**

Judges and the community can spot a "marketing site with a `Coming soon` button" from a mile away. Even a rough, ugly, working app beats a polished landing page every time.

### 2.8 External Integrations

- After the core app works, **add each external integration one at a time** (ElevenLabs, Li.Fi, x402, etc.).
- Test each integration in isolation before stacking them. Stacking broken integrations = unrecoverable debug session at 3am.

---

## Step 3 — Submission

### 3.1 Build in Public

- Post progress updates on X throughout the hackathon.
- **Tag:** `@dev3pack`, `@solana`, `@TryNoahAI`, plus any sponsor of bounties you're going for.
- This isn't just marketing — judges and sponsors actively watch these tags.

### 3.2 Deployment

- **Deploy the frontend on Vercel** (https://vercel.com) — fastest path to a public URL.
- Make sure the deployed version actually works (devnet RPC, env vars, etc.) — don't submit a localhost-only project.

### 3.3 Submission Materials Checklist

**Visual assets:**
- Logo
- Banner / cover image
- Screenshots of the app

**Architecture diagram:**
- Use **Excalidraw** (https://excalidraw.com) to draw a dApp infrastructure / workflow diagram.
- Include both **off-chain** (frontend, backend, indexers) and **on-chain** (programs, accounts) components.
- Export as a screenshot and include it in the submission.

**README on GitHub (VERY IMPORTANT):**
- Clear project description
- How to run it locally
- Tech stack
- Architecture overview
- Deployed URLs and program addresses
- Team / contributor info

**Demo video (3 minutes MAX):**
1. Project description (what is it, in one sentence)
2. Why you built it / problem solved
3. How the product works — actual demo, not slides
4. Team background (if there's time)

### 3.4 Submission Form

- **Deadline:** Fill in the submission form **before 8AM UTC on Sunday**. Set a personal deadline 2 hours earlier — submission systems get hammered at the deadline.
- **Explain the tech stack and each integration by bounty.** For each bounty you're claiming, include:
  - Specific code references (file paths, line numbers, or links)
  - Deployed contract / program addresses
  - How the integration is actually used in the product
- **Re-read every bounty's requirements** and confirm you've hit each one. Missing one criterion = disqualified from that bounty.

---

## Step 4 — Judging

During judging, the mentor's role is to help hackers stay calm and respond well to feedback.

- Be ready to demo live (and have a backup video in case wifi dies).
- Lead with the **problem**, then the **demo**, then the **tech**. Not the other way around.
- Anticipate the "why blockchain?" question — have a one-sentence answer ready.
- Be honest about what's working and what's a known limitation. Judges respect builders who know their own product's edges.

---

## Step 5 — After Hackathon

Most hackers stop building the moment they submit. The winners don't.

- **Re-build in public with the final result.** Post the final demo, the lessons learned, and what's next.
- Keep shipping — even if you didn't win, the project, the network, and the GitHub history compound.
- This step is genuinely "so important" and the most underrated part of the entire hackathon.

---

## Quick-Reference Resource Index

### Ideation
- Superteam Ideas: https://superteam.fun/build/ideas
- SendAI Ideas: https://ideas.sendai.fun/
- Colosseum Copilot: https://colosseum.com/copilot
- Past Winners: https://superteam.fun/build/past-hackathon-winners
- Colosseum Agent Projects: https://colosseum.com/agent-hackathon/projects
- Hackathon Projects (cross-ecosystem): https://hackathonprojects.dev/
- DeFi Llama: https://defillama.com
- SoleneGPT: https://solenegpt.bonfires.ai/

### Execution
- NoahAI: https://trynoah.ai
- Phantom Wallet: https://phantom.com
- Solana Faucet: https://faucet.solana.com
- solana.new: https://solana.new
- Solana Skills: https://solanaskills.com
- Awesome Solana AI: https://github.com/solana-foundation/awesome-solana-ai

### Submission
- Vercel: https://vercel.com
- Excalidraw: https://excalidraw.com
- GitHub: https://github.com

### Social Tags
- `@dev3pack`
- `@solana`
- `@TryNoahAI`

---

## Common Mentor Triggers (Decision Tree)

Use these patterns to recognize when to push specific advice:

| Hacker says... | Mentor responds with... |
|---|---|
| "I have too many ideas" | Section 1.2 — pick one that's meaningful to you, mobile-friendly, and has a path to users + liquidity |
| "Is my idea original?" | Send them to Colosseum Copilot (Section 1.3) |
| "I'm just going to make a landing page first" | Section 2.7 — STOP. Build the working app first. |
| "I don't know how to start coding" | Section 2.1 — wallet → idea → AI prompt → NoahAI |
| "Should I use mainnet?" | No. Devnet only. Section 2.2 — use a separate developer wallet. |
| "Do I need a backend?" | Only if needed. Section 2.6 — don't add complexity for its own sake. |
| "When is submission due?" | Section 3.4 — before 8AM UTC Sunday. Aim for 6AM UTC. |
| "Should I keep building after the hackathon?" | Section 5 — yes, this is where the real value compounds. |

---

## Final Note for the Agent

If a hacker is overwhelmed, the single most useful thing you can do is **narrow their scope**. The most common failure mode in hackathons is not "didn't build enough" — it's "tried to build too much and shipped nothing." Always be willing to say: *cut that feature, ship the core loop, add the rest after submission.*
