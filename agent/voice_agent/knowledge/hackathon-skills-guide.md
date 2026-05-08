# 🚀 Supercharge Your Hackathon with AI Skills

> **TL;DR:** Install these skills before you start hacking. They turn Claude (and other AI assistants) into a domain expert for the tools you'll actually be using. Less time fighting docs, more time shipping.

---

## Why install skills?

Skills are pre-packaged knowledge bundles that teach your AI assistant how to work with specific tools, APIs, and protocols. Instead of pasting docs into your prompts or watching the model hallucinate function signatures, the AI loads the right context on demand.

For a hackathon, this means:

- ⚡ **Faster iteration** — no more "is this the right method name?" loops
- 🎯 **Fewer hallucinations** — the AI uses real, current API patterns
- 🧠 **Domain expertise on tap** — voice, blockchain, design, all ready to go
- 🛠️ **Less boilerplate** — skills include working examples and best practices

**Pick the skills relevant to your stack and install them before kickoff.** Each takes a minute or two and will save you hours.

---

## 🎤 Voice & Audio

### ElevenLabs Skills
**Repo:** https://github.com/elevenlabs/skills

Build anything voice-related: text-to-speech, voice cloning, conversational agents, audio generation, real-time voice interfaces. If your hack has an audio component, this is non-negotiable.

**Use it for:** voice agents, TTS for accessibility, audio content generation, voice cloning demos.

```bash
git clone https://github.com/elevenlabs/skills.git
```

---

## ⛓️ Blockchain & Cross-Chain

### LI.FI Agent Skills — Cross-Chain & DeFi
**Repo:** https://github.com/lifinance/lifi-agent-skills

LI.FI is the cross-chain liquidity aggregator. These skills give your agent the ability to bridge, swap, and route across 30+ chains and 20+ bridges/DEXes without you reading every protocol's docs.

**Use it for:** cross-chain swaps, multi-chain DeFi agents, wallet automation, anything that touches more than one chain.

```bash
git clone https://github.com/lifinance/lifi-agent-skills.git
```

### Solana Skills (Official)
**Site:** https://solana.com/skills

The official Solana skills bundle. Covers core Solana development: programs, SPL tokens, transactions, RPC patterns, and the standard tooling. Start here if you're touching Solana at all.

**Use it for:** smart contracts/programs, SPL & Token-2022 launches, wallet integrations, on-chain queries.

### Solana Skills (Community)
**Site:** https://www.solanaskills.com/

Community-driven Solana skills with patterns, recipes, and examples that complement the official set. Battle-tested code for common hackathon patterns.

---

## 🎨 Design

### Figma Skills for MCP
**Docs:** https://help.figma.com/hc/en-us/articles/39166810751895-Figma-skills-for-MCP

Official Figma skills for the Figma MCP server. They teach Claude how to write to the Figma canvas, generate designs from your design system, implement designs as code, and connect components between Figma and your codebase. Game-changer if your team has a designer or you want polished UI without spending the whole hackathon on CSS.

**Key skills include:**
- `figma-use` — write/modify content directly in Figma files (frames, components, variables, auto-layout)
- `figma-create-new-file` — spin up new Figma files from a prompt
- `figma-generate-design` — produce designs from your design system
- `figma-implement-design` — turn Figma designs into code
- `figma-code-connect-components` — link design components to code references
- `figma-create-design-system-rules` — teach the AI your team's conventions once, reuse forever

The easiest install path: ask your AI assistant to grab the skills bundle and drop it into your skills folder.

### Claude Design (Anthropic)
**Site:** https://claude.com/

Anthropic's own design tool — generates design systems, web prototypes, slide decks, and one-pagers. Pairs naturally with Claude Code for the design → code handoff. Worth trying if no one on the team is a designer and you need polished mockups fast.

### Stitch (Google Labs) Skills
Skills like `design-md`, `enhance-prompt`, `react-components`, `shadcn-ui`, and `stitch-loop` enable an iterative design-to-code workflow. Useful if you're building React UIs and want shadcn-flavored output. Find them in the [VoltAgent collection](https://github.com/VoltAgent/awesome-agent-skills).

### web-artifacts-builder
Build elaborate, multi-component HTML artifacts using React, Tailwind, and shadcn/ui. Perfect for demo pages and interactive prototypes. Listed in the [awesome-claude-skills](https://github.com/BehiSecc/awesome-claude-skills) collection.

---

## 🛠️ Engineering Essentials

### Anthropic Official Skills
**Repo:** https://github.com/anthropics/skills

The first-party reference set. Includes `docx`, `pdf`, `pptx`, `xlsx`, `mcp-builder` (for building MCP servers), `artifacts-builder`, and more. Maintained by Anthropic — start here.

```bash
/plugin marketplace add anthropics/skills
```

### Superpowers (obra)
**Repo:** https://github.com/obra/superpowers

20+ battle-tested skills for Claude Code, including TDD workflows, debugging patterns, and collaboration helpers. Adds `/brainstorm`, `/write-plan`, `/execute-plan` commands.

```bash
/plugin marketplace add obra/superpowers-marketplace
```

### Composio Connect Apps
**Repo:** https://github.com/ComposioHQ/awesome-claude-skills

Lets your AI actually *do things* — send emails, create issues, post to Slack, push to 1000+ apps. If your hack involves real-world integrations (notifications, automations, workflows), this is the fastest path.

---

## 🔒 Security & Secrets

### varlock-claude-skill
Secure environment variable management — keeps secrets out of Claude sessions, terminals, logs, and git commits. Run this for any project that touches API keys (i.e., all of them).

### vibesec
Helps the AI write secure code by preventing common vulns: IDOR, XSS, SQL injection, SSRF, weak auth. Approaches code from a bug-hunter's perspective.

Both are linked from [BehiSecc/awesome-claude-skills](https://github.com/BehiSecc/awesome-claude-skills).

---

## 🎬 Media & Content

### Claude Code Video Toolkit
AI-native video production: Remotion, ElevenLabs, FFmpeg, Playwright skills bundled together. Great for demo videos and pitch reels.

### VideoDB Skills
Ingest, search, edit, generate, and stream video & audio. Useful if your hack involves any video processing.

### claude-epub-skill / revealjs-skill
Convert markdown to EPUB ebooks, or generate professional Reveal.js presentations from prose. Both useful for shipping polished pitch artifacts.

---

## 🔧 How to install skills (Claude Code)

Most skills follow the same pattern. For each repo:

1. Clone or download the skill repository (or use `/plugin marketplace add <repo>`)
2. Skills go in your skills directory:
   - macOS/Linux: `~/.claude/skills/`
   - Windows: `%USERPROFILE%\.claude\skills\`
3. Restart Claude Code (or your AI client)
4. Skills auto-load by relevance — no manual activation needed

```bash
# Example: install the core hackathon set
mkdir -p ~/.claude/skills && cd ~/.claude/skills

git clone https://github.com/elevenlabs/skills.git elevenlabs
git clone https://github.com/lifinance/lifi-agent-skills.git lifi
git clone https://github.com/obra/superpowers superpowers
# Plus: solana.com/skills, solanaskills.com, Figma skills via help docs
```

> ⚠️ **Security note:** Skills can execute code in your AI's environment. Only install from sources you trust — the official repos linked above are safe; be careful with random forks.

---

## 📚 Curated skill marketplaces

If you want to browse the full ecosystem (1000+ skills total):

- **[anthropics/skills](https://github.com/anthropics/skills)** — official, foundational
- **[VoltAgent/awesome-agent-skills](https://github.com/VoltAgent/awesome-agent-skills)** — official skills from Anthropic, Google, Vercel, Stripe, Cloudflare, Netlify, Figma, etc.
- **[ComposioHQ/awesome-claude-skills](https://github.com/ComposioHQ/awesome-claude-skills)** — 1000+ production-ready skills, automation-heavy
- **[BehiSecc/awesome-claude-skills](https://github.com/BehiSecc/awesome-claude-skills)** — broad community-curated list
- **[karanb192/awesome-claude-skills](https://github.com/karanb192/awesome-claude-skills)** — 50+ verified, actively maintained
- **[hesreallyhim/awesome-claude-code](https://github.com/hesreallyhim/awesome-claude-code)** — skills + hooks + slash commands + plugins for Claude Code

---

## ✅ Pre-hack checklist

- [ ] Skills relevant to your stack are installed
- [ ] Claude Code (or your AI client) restarted after install
- [ ] API keys ready: ElevenLabs, RPC endpoints, wallets, Figma access tokens, etc.
- [ ] Tested skill loading by asking your AI a domain-specific question
- [ ] Bookmarked the skill repos in case you need to grep examples
- [ ] Secrets/env vars handled via `varlock` or equivalent — not pasted into prompts

---

## 🏆 Pro tips

1. **Be explicit about which skill to use.** "Use the LI.FI skill to build a cross-chain swap" beats "build a swap."
2. **Skills compose.** A voice agent (ElevenLabs) that triggers a Solana transaction and posts the receipt to Slack (Composio) is three skills working in concert. The AI handles the handoff.
3. **Read the SKILL.md files.** Each skill has a top-level description in its `SKILL.md`. Skim them so you know what's available without re-prompting.
4. **Don't over-install.** Each skill adds metadata to context. Install what fits your stack; skip the rest.
5. **Report bugs upstream.** Stale skill? Open an issue. Maintainers care.

---

**Now go build something. Ship fast. 🛠️**
