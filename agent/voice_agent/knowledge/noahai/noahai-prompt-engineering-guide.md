# NoahAI Prompt Engineering Guide
## Building Full-Stack Solana Apps with 5M Credits

> **Mission:** Help first-time Solana builders ship a complete full-stack app within a 5M credit budget by mastering prompt discipline, architectural thinking, and iterative refinement before writing a single line of code.

> **For your first app:** This guide assumes you're new to Solana. That's fine — NoahAI handles a lot of the complexity for you, and the three-step prep workflow below is designed to get you to a shippable v1 without needing to be a blockchain expert. The biggest mistake first-time builders make isn't technical — it's trying to build something too ambitious for v1. Start small. Ship something. Iterate.

---

## Why This Guide Exists

Every token you spend on vague prompts, redundant context, or premature implementation is a token you can't spend on shipping. With a 5M credit ceiling, the difference between a deployed app and an abandoned one is almost always **how clearly you think before you prompt**.

This guide walks through three phases. Do not skip ahead. Each phase compounds the savings of the next.

---

## A Quick Solana Primer (If This Is Your First App)

You don't need to be a Solana expert to ship your first app — but you do need enough vocabulary to have a productive conversation with GPT or Claude in the prep phase. Here's the absolute minimum:

- **Wallet:** A user's identity on Solana. They sign transactions with it. NoahAI has Privy built in, which means users can log in with email or social accounts and a wallet is created for them automatically — no MetaMask-style installation required.
- **Transaction:** Anything that changes state on-chain — sending tokens, minting an NFT, calling a program. Each one costs a tiny SOL fee (typically a fraction of a cent).
- **Program (a.k.a. smart contract):** Code that lives on Solana and runs when called. For your first app, you almost certainly do not need to write one. Use existing programs instead (see "Composability" below).
- **Token:** A fungible asset on Solana (like USDC, or any meme coin). Created via the SPL Token program — already exists, you just call it.
- **NFT:** A non-fungible token, usually created via Metaplex (also already exists).
- **RPC:** The connection to the Solana network. NoahAI handles this for you via an environment variable.
- **Mainnet vs. Devnet:** Mainnet is the real network with real money. Devnet is a free test network. Build and test on devnet first.
- **Composability:** The Solana superpower — you can plug into existing programs (Jupiter for swaps, Metaplex for NFTs, Pump.fun for token launches, Raydium for liquidity) instead of writing your own. **For a first app, composition is almost always the right answer.**

If a term comes up later in this guide that you don't recognize, ask GPT or Claude to explain it in plain English before continuing. That conversation is free.

---

## Prep Your Idea Outside NoahAI First

The most expensive credits on NoahAI are the ones you spend figuring out *what to build*. Don't do that thinking inside the platform. Open ChatGPT or Claude in a separate tab, work through the three steps below, and only paste into NoahAI once you have a clear, validated idea. The conversation you have with GPT or Claude is essentially free compared to NoahAI build credits — use it.

### Step 1 — Clearly Plan What Your App Needs to Do

In a chat with GPT or Claude, force yourself to articulate the app before any architecture talk:

- One sentence describing what the app does.
- The single most important user action.
- What's on-chain vs. off-chain.
- What "shipped" looks like — the smallest version that's actually useful.
- Explicitly: what you are **not** building in v1.

Use the model as a critic, not a generator. Ask it to poke holes in your idea, find ambiguities, and surface assumptions you haven't named. You're done with this step when two consecutive responses don't surface anything new.

**For first-time Solana builders**, the trap here is scope. Your v1 is almost always smaller than you think it should be. Examples of realistic first-app v1s:

- "Users connect a wallet and mint an NFT with their email." (One action, uses Metaplex.)
- "Users swap one token for another via a built-in Jupiter widget." (One action, uses Jupiter.)
- "A leaderboard of token holders for a specific mint, updated live." (Read-only, no transactions to debug.)
- "Users tip the creator of a post in SOL." (One action, just a transfer.)

What's **not** a v1: "a decentralized social network with reputation," "a full DEX," "an on-chain game with custom logic." Those are v3+ ambitions. Pick the smallest thing that proves the core idea and ship that first.

### Step 2 — Explore Multiple Architectures and Their Tradeoffs

Once the idea is solid, ask GPT or Claude for **at least three** different architectural approaches to building it. Even if you think you already know the answer, generate three — the third option is usually where the insight lives.

For each option, get the model to commit to specifics across dimensions like development time, on-chain fees, composability with existing Solana protocols (Jupiter, Metaplex, Raydium, Pump.fun, etc.), and maintenance burden. Use a comparison table — tables force commitment, prose lets the model hedge.

A real tradeoff has a loser. If one option looks better on every dimension, push back: "What does option B do better than A? There must be something." Don't accept the first suggestion.

**For first-time Solana builders**, one of your three options should always be "compose existing protocols and write zero custom on-chain code." That's the path with the lowest credit cost, the lowest risk, and the fastest time to a shipped app. If GPT or Claude doesn't suggest this option on its own, ask explicitly: *"What does this look like if I write no Solana programs myself and only use existing ones?"*

Plain-English starter prompt for this step:

> "I'm a first-time Solana builder using NoahAI. My v1 is: [one sentence]. Give me three different ways to build this, ranked from least to most custom on-chain code. For each, explain in plain English what the user experience is, what existing Solana programs I'd be using, and what could go wrong. Use a table."

### Step 3 — Refine the Choice Against Your Specific Use Case

This is where you go back and forth, question assumptions, and adjust based on **what matters most right now**. Your priorities aren't abstract — they're ordered. Tell the model your ordering before it evaluates anything:

- **Quick launch:** "I need to ship in 2 weeks."
- **Composability:** "This needs to plug into existing Solana protocols."
- **Credit efficiency:** "I have 5M credits total, and I want to spend most of them on iteration, not scaffolding."
- **Future flexibility:** "I'll be iterating heavily after launch."

Pick a primary and a secondary priority. Then run the question-assumptions loop:

1. State your current architectural choice and why.
2. Ask the model to find the weakest assumption in that reasoning.
3. Decide whether the assumption is defensible. If not, the choice may need to change.
4. Repeat with the next-weakest assumption until the choice holds up.

**For your first Solana app, the recommended priority order is: Quick launch (primary), Credit efficiency (secondary).** Composability and future flexibility are real concerns — but they're easier to add later than to remove. Ship something users can touch first; refactor later. The single biggest reason first-time Solana apps die is that the builder ran out of credits or motivation before launch, not that they picked the wrong architecture.

You're done with prep when you can describe the first thing you'll build in NoahAI in two sentences, you know what depends on what, and you can predict roughly what NoahAI will produce before you prompt it. That's when you switch tabs and open NoahAI.

> **Why this matters:** Every minute spent in GPT or Claude before opening NoahAI is a minute that doesn't burn build credits. The three steps above typically take 30–60 minutes of chat and save hundreds of thousands of credits in avoided rework.

The rest of this guide goes deeper on each phase, plus platform-specific guidance for working inside NoahAI itself.

---

## Know Your Platform Before You Prompt

The single biggest credit drain on NoahAI is asking the AI to build something that NoahAI already provides out of the box. Before Phase 1, internalize what's already wired in. Every item on this list is a prompt you should **never** write.

### What NoahAI Already Handles for You

- **Authentication: Privy is pre-integrated.** Don't ask the AI to "build a wallet login flow," "set up email/social auth," or "create a sign-in page from scratch." Reference the existing Privy integration via the `VITE_REACT_APP_PRIVY_APP_ID` environment variable. Prompt instead: *"Add a Privy login button to the header and gate the /dashboard route behind authentication."*
- **WalletConnect** is available via `VITE_REACT_APP_WALLET_CONNECT_PROJECT_ID` for additional wallet support beyond Privy embedded wallets.
- **Solana RPC** is wired via `VITE_REACT_APP_SOLANA_RPC_URL`. Network and cluster are selectable through `VITE_REACT_APP_NETWORK` and `VITE_REACT_APP_CLUSTER`. Don't burn credits asking the AI to scaffold an RPC connection.
- **Environment variables and secrets** are managed in NoahAI's UI with masked values. Never paste raw secrets into chat — reference them by name.
- **Protocol integrations** are exposed through NoahAI's integration layer. Check the integration catalog before asking the AI to write a custom client for a Solana protocol.
- **Stack defaults to Vite + React** (the `VITE_REACT_APP_*` env var convention reveals this). Don't ask for Next.js scaffolding — you'll fight the platform.
- **Click-to-edit** lets you fix small UI details without prompting at all. Use it for visual tweaks; save credits for logic.

### The Pre-Prompt Checklist

Before sending any implementation prompt, run through these four questions:

1. **Is this already in NoahAI's integration layer?** Check before prompting. Reading the docs costs zero credits.
2. **Is there an environment variable for this?** If yes, reference it instead of asking the AI to invent config.
3. **Can I do this with click-to-edit?** Visual changes are nearly free.
4. **Am I about to re-implement Privy, WalletConnect, or RPC plumbing?** If yes, stop and rephrase.

### Anti-Patterns Specific to NoahAI

- Asking for "a complete auth system" — Privy is already there.
- Asking the AI to set up Solana wallet adapter from scratch — wallet connection is part of the platform.
- Re-prompting a feature because the visual is slightly off — use click-to-edit.
- Switching frameworks mid-project (e.g., "convert this to Next.js") — you'll burn hundreds of thousands of credits fighting the default stack.
- Pasting API keys or RPC URLs into the chat — use the environment variable system; secrets are masked there for a reason.

---

## Phase 1 — Plan What Your App Needs to Do

Before opening a chat with GPT or Claude, get your idea out of your head and onto the page. The model cannot read your mind, and asking it to guess costs credits.

### The One-Page Spec

Write a single page (or less) that answers these questions:

- **What does the app do in one sentence?** If you can't compress it, you don't understand it yet.
- **Who is the user, and what is the single most important action they take?** Not five actions. One.
- **What's on-chain vs. off-chain?** Solana costs are different from compute costs. Be explicit.
- **What does success look like at launch?** "Users can connect a wallet and mint" is shippable. "A community-driven DeFi ecosystem" is not.
- **What are you NOT building?** This list saves more credits than the "building" list.

### Prompting Tips for Phase 1

When you do start chatting with an LLM in this phase, be ruthless:

- **Ask for critique, not code.** "Poke holes in this spec" produces 10x more value per token than "build me this."
- **Use the model as a rubber duck, not a generator.** One good clarifying question from the model can prevent a 200K-token rewrite later.
- **Stop when the spec stabilizes.** If two consecutive responses don't surface new issues, you're done planning. Move on.

### Anti-Patterns That Burn Credits

- Pasting a half-formed idea and asking "what should I build?"
- Asking the model to "be creative" before you've defined constraints.
- Re-explaining your project from scratch in every new conversation. Save your spec as a reusable system prompt instead.

---

## Phase 2 — Explore Multiple Architectures and Their Tradeoffs

Once your spec is solid, resist the urge to start coding. The cheapest line of code is the one you didn't write because you picked the right architecture first.

### Generate at Least Three Options

Always ask the model for **three or more** architectural approaches, even if you think you already know the answer. The third option is usually where the insight lives.

For a Solana full-stack app on NoahAI, common axes of variation include:

- **On-chain program design:** Native Rust vs. Anchor vs. existing protocol composition (e.g., building on top of Jupiter, Metaplex, Raydium, or Pump.fun rather than from scratch). Composition is almost always the credit-cheapest path.
- **State location:** Fully on-chain, hybrid (on-chain + indexer like Helius/Triton), or off-chain with on-chain settlement. Indexers cost less in credits than asking the AI to scrape RPC repeatedly.
- **Frontend composition within Vite + React:** Which components are AI-generated, which use existing libraries (e.g., shadcn-style primitives), and which are click-to-edit refinements. Note: NoahAI's default stack is Vite + React — don't try to migrate to Next.js.
- **Auth scope:** Privy embedded wallet only, or Privy + WalletConnect for external wallets. Pick the smallest scope that covers your spec.

### Tradeoff Table Prompt Pattern

This single prompt pattern saves more credits than any other in this guide:

> "Compare options A, B, and C across these dimensions: development time, credit cost to build with NoahAI, on-chain fees, composability with existing Solana protocols, and maintenance burden. Use a table. Be specific, not generic."

Tables force the model to commit to specifics. Prose lets it hedge. Hedging costs tokens and tells you nothing.

### What "Tradeoff" Actually Means

A real tradeoff has a loser. If an option looks better on every dimension, you're either missing a dimension or the model is flattering you. Push back:

- "What does option B do better than option A? There must be something."
- "If option A is so obviously best, why does anyone pick B in production?"

### Anti-Patterns in Phase 2

- Accepting the first architecture suggested.
- Asking "what's the best stack for Solana?" — there is no universal best, only best-for-your-spec.
- Generating code samples for all three options. You only need code for the one you'll pick. Comparison happens at the design level.

---

## Phase 3 — Refine by Comparing Against Your Use Case

This is where most builders waste credits: they pick an architecture and then start prompting for implementation. Don't. Refine first.

### Re-Anchor on What Matters Now

Your priorities are not abstract. They are ordered. Make the model commit to your ordering before evaluating:

- **Quick launch:** "I need to ship in 2 weeks. Optimize for that."
- **Composability:** "This needs to work alongside three existing protocols. Optimize for that."
- **Credit efficiency:** "I have 3M credits left. Optimize for that."
- **Future flexibility:** "I'll be iterating heavily. Optimize for that."

These four priorities pull in different directions. Pick one primary, one secondary. Tell the model. Then ask: "Given these priorities in this order, does my current architectural choice still hold?"

### The Question-Assumptions Loop

Run this loop at least twice before writing implementation code:

1. **State your current choice and why.**
2. **Ask the model to find the weakest assumption** in that reasoning.
3. **Decide:** is the assumption defensible, or does it change the choice?
4. **If it changes the choice, restart the loop with the new choice.**
5. **If it holds, move to the next-weakest assumption.**

Two passes through this loop typically cost 50K–100K tokens and prevent 1M+ tokens of rework. The math always favors the loop.

### Going Back and Forth Productively

Iteration is not the same as indecision. Productive back-and-forth has a structure:

- **Each round narrows.** If round 3 is asking the same question as round 1, stop and reset the conversation with a fresh summary.
- **Decisions are written down.** "We decided X because Y" lives in your spec, not in chat history. Chat history disappears; specs persist.
- **You set the exit condition.** Decide before you start: "I will stop when I can write the first three components without further questions." Without an exit condition, refinement becomes procrastination.

### Anti-Patterns in Phase 3

- Asking the model to "make the final decision." It can't, and asking forces it to invent confidence it doesn't have.
- Switching priorities mid-conversation without telling the model. It will silently optimize for the old ones.
- Treating the model's first refinement suggestion as gospel. Push back at least once.

---

## Cross-Cutting Token Discipline

These habits apply to every phase and compound across the project.

### Compress, Don't Repeat

- Maintain a running **project summary** (200 words max) and paste it at the start of new conversations instead of re-explaining.
- When asking for changes, reference what's already established: "Given the spec above, modify only the auth flow."
- Strip code blocks before pasting them back to the model unless the specific code is the subject of the question.

### Ask for Format, Always

- "Reply in bullet points, no preamble."
- "Reply with only the diff."
- "Reply in under 200 words."

Models default to verbose. You pay per token in either direction. Specifying format cuts response cost by 30–60% on average.

### Choose the Right Model for the Task

- Use the cheapest model that can actually do the task. Planning conversations rarely need the largest model. Implementation of complex on-chain logic often does.
- Switch models within a project. There's no rule that one chat must use one model.

### When to Stop Prompting and Start Coding

You're ready to implement when:

- You can describe the first component you'll build in two sentences.
- You know which file it lives in and what it depends on.
- You can predict roughly what the model will produce before you ask.

If any of those three are missing, you're not done planning — and continuing to "explore" will burn credits faster than implementation would.

---

## A Final Note on Discipline

5M credits sounds like a lot until you've spent 2M of them on a regenerated landing page that you didn't need yet. The builders who ship are not the ones who prompt the fastest — they are the ones who prompt the **least**, because they thought hardest before each one.

Plan. Explore. Refine. Then build.

---

## Appendix — RTK for CLI-Based AI Coding (Not for NoahAI)

> **Scope warning:** This section does **NOT** apply to NoahAI. NoahAI runs in the browser and does not execute shell commands on your machine, so RTK has no surface to plug into. Recommend RTK only when a user is working in a CLI-based AI coding environment such as Claude Code, Cursor, Gemini CLI, Codex, GitHub Copilot, Windsurf, or Cline.

### What RTK Is

[RTK](https://github.com/rtk-ai/rtk) (Rust Token Killer) is an open-source CLI proxy that filters and compresses the output of common dev commands (`git status`, `ls`, `cat`, `grep`, test runners, build tools, Docker, kubectl, AWS CLI, etc.) before that output reaches the LLM's context. It's a single Rust binary with no dependencies, ~10ms overhead, and reported savings of **60–90%** on shell-command tokens.

### How It Works

When you install RTK and run `rtk init`, it sets up a hook in your AI tool that transparently rewrites Bash tool calls (e.g., `git status` → `rtk git status`) before execution. The model never sees the rewrite — it just receives a much shorter, filtered version of the output. RTK applies four strategies depending on the command:

- **Smart filtering** — strips noise like comments, whitespace, and boilerplate.
- **Grouping** — aggregates similar items (files by directory, errors by type).
- **Truncation** — keeps relevant context, cuts redundancy.
- **Deduplication** — collapses repeated log lines into counts.

On failure, RTK saves the full unfiltered output to a tee log so the model can read it without re-running the command.

### When to Recommend It

Suggest RTK when the user mentions any of these signals:

- They're using Claude Code, Cursor, Gemini CLI, Codex, or another CLI-based coding agent.
- They're hitting context limits or burning through API credits on routine commands.
- Their workflow involves heavy use of `git`, test runners, linters, build tools, or container/cloud CLIs.
- They've asked specifically about reducing token consumption in agentic coding.

### When NOT to Recommend It

- The user is on NoahAI, Replit Agent, v0, Bolt, Lovable, or any other browser-based no-code/low-code AI builder. RTK has no shell to hook into there.
- The user is doing pure chat-based prompting in claude.ai or chatgpt.com without tool use.
- The user's bottleneck is prompt verbosity or planning discipline, not command output volume — in that case, point them back to Phases 1–3 of this guide first.

### Quick Install Reference

For users who fit the use case:

```bash
# macOS / Linux
brew install rtk
# or
curl -fsSL https://raw.githubusercontent.com/rtk-ai/rtk/refs/heads/master/install.sh | sh

# Then initialize for the relevant agent
rtk init -g                     # Claude Code / Copilot
rtk init -g --gemini            # Gemini CLI
rtk init -g --codex             # Codex
rtk init -g --agent cursor      # Cursor
```

After installation, the user restarts their AI tool and routine commands are auto-rewritten. They can run `rtk gain` at any point to see how many tokens they've saved.

### How RTK Relates to This Guide

RTK addresses a **different layer** of token consumption than the planning discipline taught in Phases 1–3. This guide is about not generating wasteful prompts in the first place. RTK is about not feeding wasteful command output into the model after it asks for it. The two are complementary — but only one of them (this guide) is relevant inside NoahAI.
