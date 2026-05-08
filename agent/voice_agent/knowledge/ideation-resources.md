# Ideation Resources for AI Mentor Agent

A curated collection of resources to help builders ideate, validate, and refine project ideas — primarily focused on the Solana ecosystem, hackathons, and AI agents.

---

## 1. Colosseum Copilot

**URL:** https://colosseum.com/copilot

A research skill (installable into Claude Code, Codex, or OpenClaw) for deep crypto product research. Lets builders pressure-test startup ideas against 5,400+ hackathon submissions, 65+ curated crypto sources, and live ecosystem data from The Grid (6,300+ products).

**What it's good for during ideation:**
- "Should I build this?" — competitor scan + landscape analysis + evidence-based assessment
- Checking if an idea has already been built (surfaces project, hackathon, and what was shipped)
- Mapping a builder's skills/background to verticals where they have a genuine competitive edge
- Getting an honest, adversarial take on a weak idea (ask it to argue against yours)
- Tracing ideas to their origins through 65+ curated sources (theory → live implementations)
- Spotting which niches are heating up vs. cooling down across hackathons

**What's inside:**
- 5,400+ Solana hackathon projects with tech stack, categories, verticals, semantic search + filters
- Coverage across four hackathons: Renaissance, Radar, Breakout, Cypherpunk
- Topic clusters: AI Agents, DEX Infra, DeFi, Gaming, Payments, DePIN
- Direct competitor alerts (e.g., Helius, Squads, Kamino, Sphere)
- Archive Library: cypherpunk writings (Satoshi, Nick Szabo), research firms (Paradigm, a16z Crypto, Multicoin, Electric Capital), Paul Graham essays, Solana protocol docs (Jupiter, Orca, Drift, Helius, Jito, Firedancer, OtterSec)

**Install:** `npx skills add ColosseumOrg/colosseum-copilot`

**Docs:** https://docs.colosseum.com/copilot

---

## 2. Colosseum Agent Hackathon — Projects

**URL:** https://colosseum.com/agent-hackathon/projects

Live directory of 750+ projects from Colosseum's first hackathon where AI agents compete. Excellent reference for what AI agents on Solana actually look like in practice — useful for spotting gaps, avoiding duplication, and seeing emerging patterns.

**Recurring themes across submissions (useful for ideation):**

- **Autonomous DeFi execution & risk management** — agents monitoring lending positions, simulating repays/rebalances, executing trades (e.g. DeFi Risk Guardian, SIDEX, Super Router, CrewDegen Arena, Xirion)
- **Agent-to-agent economies** — marketplaces where agents publish/execute tasks, micropayments via x402, escrow, reputation (e.g. SugarClawdy, MoltyDEX, 1lyAgent, SolSkill)
- **Verifiable AI reasoning / on-chain memory** — committing AI thought processes, reasoning traces, or memory state on-chain (e.g. SOLPRISM, Clude, Proof of Work activity log)
- **Security & monitoring swarms** — multi-agent systems for threat detection, scam/honeypot detection, transaction simulation (e.g. GUARDIAN, BlinkGuard, Eremos)
- **Agent-native infrastructure** — launchpads, DEX aggregators, identity layers, social networks built specifically *for* agents rather than humans (e.g. Blowfish, ZNAP, Identity Prism, Moltlets World)
- **Compliance & audit automation** — jurisdiction-specific tax/audit agents indexing on-chain + CEX data (e.g. AuditSwarm)
- **Prediction market intelligence** — social/AI oracles analyzing markets in real time (e.g. Polymira, Clodds)
- **Agent gaming / in-game agents** — coordinating real-time agents inside game worlds (e.g. ClaudeCraft for Minecraft)

**How to use this with mentees:**
- Have them browse and identify 3 projects in their target vertical
- Ask: "What's missing from these? What would you build differently?"
- Use it as a "prior art" check before committing to a direction

---

## 3. Superteam Build — Ideas

**URL:** https://superteam.fun/build/ideas

A curated catalog of project ideas across Solana, contributed by founders in the ecosystem. Many ideas come with equity-free grants attached — meaning they're ideas Solana founders are actively willing to fund someone to build.

**Categories typically covered:** DeFi, NFTs, Payments, Consumer dApps, Infrastructure, Tooling, Gaming, and more.

**Why this is valuable during ideation:**
- Ideas are filtered for ecosystem relevance (not random brainstorms)
- Each idea is paired with someone willing to mentor or fund it
- Useful for builders who have skills but no clear thesis yet

---

## 4. SendAI Ideas

**URL:** https://ideas.sendai.fun/

A curated list of project ideas at the intersection of Solana and AI, maintained by SendAI. Specifically tailored for hackathon builders looking to ship AI-native projects on Solana.

**When to use this:**
- The mentee has decided on AI + Solana but doesn't have a specific wedge
- They want to see what the SendAI team (one of the leading AI-on-Solana groups) considers worth building
- For benchmarking against the broader Solana AI agent landscape

**Related:**
- SendAI on X: https://x.com/sendaifun
- SendAI GitHub: https://github.com/sendaifun

> Note: Browse the URL directly — the list is rendered dynamically.

---

## 5. Superteam — Past Hackathon Winners

**URL:** https://superteam.fun/build/past-hackathon-winners

150+ winning projects from past Solana global hackathons, with presentations, demo videos, and post-mortems on what they did right.

**Why this is one of the highest-leverage ideation resources:**
- **Pattern recognition** — seeing what consistently wins reveals what judges value
- **Competitive research** — know what already exists at a high quality bar
- **Format learning** — watching demo videos teaches how to present an idea, not just build it
- **Calibration** — sets a realistic bar for "what hackathon-winning quality actually looks like"

**Workflow with mentees:**
1. Pick the hackathon track most relevant to their interests
2. Watch 3–5 winning demos in that track
3. Reverse-engineer: What problem? What insight? What demo moment sold it?
4. Then ideate — knowing the bar.

> Note: Some GitHub/presentation links may be inactive (projects deleted or no longer open-sourced).

---

## 6. RadiantsDAO Post (X / Twitter)

**URL:** https://x.com/RadiantsDAO/status/2049549104175268000

Direct content could not be fetched (X blocks automated retrieval). The mentee/agent should open the link directly to read the post.

**Suggested handling for the mentor agent:** When this resource is referenced, prompt the user to share the post's content directly (paste text or screenshot) so it can be incorporated into ideation discussions.

---

## How the Mentor Agent Should Use These Resources

A suggested ideation flow when working with a mentee:

1. **Diverge** — Send them to **Superteam Build Ideas** and **SendAI Ideas** to expand their option space.
2. **Calibrate** — Send them to **Superteam Past Hackathon Winners** to see the quality bar.
3. **Stress-test** — Use **Colosseum Copilot** to check for prior art, competitors, and gaps.
4. **Validate against reality** — Browse the **Colosseum Agent Hackathon Projects** to see what's been built recently and where the genuine whitespace is.
5. **Converge** — Help the mentee write a one-paragraph thesis covering: problem, who it's for, why now, what's the unfair advantage, why it's not already a crowded space.

The goal is not to find a "novel" idea — it's to find an idea where the mentee has a genuine edge and the timing is right.
