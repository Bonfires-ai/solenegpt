"""
Generate an Excalidraw presentation deck for teaching x402 on Solana to
hackathon participants.

Each slide is a 1600x900 Frame, laid out in a horizontal strip so the
"Presentation Mode" in Excalidraw walks through them in order.

Run:
    python scripts/gen-x402-deck.py
Output:
    docs/x402-solana-presentation.excalidraw
"""

from __future__ import annotations

import json
import random
import string
import time
from pathlib import Path
from typing import Any

# ---------- Layout constants ----------
SLIDE_W = 1600
SLIDE_H = 900
SLIDE_GAP = 200  # horizontal gap between slides

# Color palette
INK = "#1e1e1e"
MUTED = "#6c757d"
PURPLE = "#7950f2"
PURPLE_DARK = "#5f3dc4"
PURPLE_BG = "#f3f0ff"
GREEN = "#2f9e44"
GREEN_BG = "#ebfbee"
RED = "#e03131"
RED_BG = "#fff5f5"
BLUE = "#1971c2"
BLUE_BG = "#e7f5ff"
ORANGE = "#f08c00"
ORANGE_BG = "#fff4e6"
YELLOW_BG = "#fff9db"
GREY_BG = "#f1f3f5"


def gen_id() -> str:
    return "".join(random.choices(string.ascii_letters + string.digits, k=20))


def base_props(frame_id: str | None = None) -> dict[str, Any]:
    return {
        "id": gen_id(),
        "angle": 0,
        "strokeColor": INK,
        "backgroundColor": "transparent",
        "fillStyle": "solid",
        "strokeWidth": 2,
        "strokeStyle": "solid",
        "roughness": 1,
        "opacity": 100,
        "groupIds": [],
        "frameId": frame_id,
        "roundness": None,
        "seed": random.randint(1, 2_000_000_000),
        "version": 1,
        "versionNonce": random.randint(1, 2_000_000_000),
        "isDeleted": False,
        "boundElements": [],
        "updated": int(time.time() * 1000),
        "link": None,
        "locked": False,
    }


def text(
    x: float,
    y: float,
    s: str,
    *,
    size: int = 24,
    color: str = INK,
    align: str = "left",
    width: float | None = None,
    bold: bool = False,
    frame_id: str | None = None,
    font: int = 5,  # 1=Virgil, 5=Excalifont, 7=Cascadia mono
) -> dict[str, Any]:
    lines = s.split("\n")
    avg_char = size * 0.55 if font != 7 else size * 0.62
    if width is None:
        width = max(len(line) * avg_char for line in lines) + 4
    height = size * 1.25 * len(lines)
    e = base_props(frame_id)
    e.update(
        {
            "type": "text",
            "x": x,
            "y": y,
            "width": width,
            "height": height,
            "strokeColor": color,
            "strokeWidth": 1,
            "fontSize": size,
            "fontFamily": font,
            "text": s,
            "textAlign": align,
            "verticalAlign": "top",
            "containerId": None,
            "originalText": s,
            "lineHeight": 1.25,
            "autoResize": True,
        }
    )
    return e


def rect(
    x: float,
    y: float,
    w: float,
    h: float,
    *,
    stroke: str = INK,
    bg: str = "transparent",
    fill: str = "solid",
    stroke_width: int = 2,
    stroke_style: str = "solid",
    rounded: bool = True,
    frame_id: str | None = None,
) -> dict[str, Any]:
    e = base_props(frame_id)
    e.update(
        {
            "type": "rectangle",
            "x": x,
            "y": y,
            "width": w,
            "height": h,
            "strokeColor": stroke,
            "backgroundColor": bg,
            "fillStyle": fill,
            "strokeWidth": stroke_width,
            "strokeStyle": stroke_style,
            "roundness": {"type": 3} if rounded else None,
        }
    )
    return e


def ellipse(
    x: float, y: float, w: float, h: float, *, stroke: str = INK, bg: str = "transparent",
    frame_id: str | None = None,
) -> dict[str, Any]:
    e = base_props(frame_id)
    e.update(
        {
            "type": "ellipse",
            "x": x,
            "y": y,
            "width": w,
            "height": h,
            "strokeColor": stroke,
            "backgroundColor": bg,
            "fillStyle": "solid",
        }
    )
    return e


def line(
    x1: float, y1: float, x2: float, y2: float, *, stroke: str = INK, stroke_width: int = 2,
    stroke_style: str = "solid", frame_id: str | None = None,
) -> dict[str, Any]:
    e = base_props(frame_id)
    e.update(
        {
            "type": "line",
            "x": x1,
            "y": y1,
            "width": x2 - x1,
            "height": y2 - y1,
            "strokeColor": stroke,
            "strokeWidth": stroke_width,
            "strokeStyle": stroke_style,
            "points": [[0, 0], [x2 - x1, y2 - y1]],
            "lastCommittedPoint": None,
            "startBinding": None,
            "endBinding": None,
        }
    )
    return e


def arrow(
    x1: float, y1: float, x2: float, y2: float, *, stroke: str = INK, stroke_width: int = 2,
    label: str | None = None, frame_id: str | None = None,
) -> list[dict[str, Any]]:
    e = base_props(frame_id)
    e.update(
        {
            "type": "arrow",
            "x": x1,
            "y": y1,
            "width": x2 - x1,
            "height": y2 - y1,
            "strokeColor": stroke,
            "strokeWidth": stroke_width,
            "points": [[0, 0], [x2 - x1, y2 - y1]],
            "lastCommittedPoint": None,
            "startBinding": None,
            "endBinding": None,
            "startArrowhead": None,
            "endArrowhead": "arrow",
            "elbowed": False,
        }
    )
    elements = [e]
    if label:
        mx = (x1 + x2) / 2
        my = (y1 + y2) / 2 - 18
        elements.append(text(mx - len(label) * 6, my, label, size=16, color=stroke, frame_id=frame_id))
    return elements


def frame(x: float, y: float, name: str) -> tuple[dict[str, Any], str]:
    e = base_props(None)
    e.update(
        {
            "type": "frame",
            "x": x,
            "y": y,
            "width": SLIDE_W,
            "height": SLIDE_H,
            "name": name,
            "strokeColor": "#bbbbbb",
            "backgroundColor": "transparent",
            "strokeWidth": 1,
        }
    )
    return e, e["id"]


# ---------- Slide builders ----------


def slide_pos(idx: int) -> tuple[float, float]:
    """Lay slides out in a 4-column grid so the canvas isn't 25k wide."""
    cols = 4
    col = idx % cols
    row = idx // cols
    x = col * (SLIDE_W + SLIDE_GAP)
    y = row * (SLIDE_H + SLIDE_GAP)
    return x, y


def slide_title(fid: str, x0: float, y0: float, number: int, title: str, subtitle: str | None = None) -> list:
    out: list[Any] = []
    # Slide number badge
    out.append(rect(x0 + 60, y0 + 60, 80, 80, stroke=PURPLE, bg=PURPLE, fill="solid", frame_id=fid))
    out.append(text(x0 + 80, y0 + 78, str(number), size=44, color="#ffffff", bold=True, frame_id=fid))
    # Title
    out.append(text(x0 + 170, y0 + 70, title, size=48, color=INK, bold=True, frame_id=fid))
    # Underline
    out.append(line(x0 + 60, y0 + 165, x0 + SLIDE_W - 60, y0 + 165, stroke=PURPLE, stroke_width=3, frame_id=fid))
    if subtitle:
        out.append(text(x0 + 170, y0 + 130, subtitle, size=22, color=MUTED, frame_id=fid))
    return out


def slide_footer(fid: str, x0: float, y0: float, label: str) -> list:
    return [
        text(x0 + 60, y0 + SLIDE_H - 50, label, size=14, color=MUTED, frame_id=fid),
        text(x0 + SLIDE_W - 250, y0 + SLIDE_H - 50, "x402 on Solana", size=14, color=MUTED, frame_id=fid),
    ]


# ============================================================
# SLIDES
# ============================================================


def build() -> list[dict[str, Any]]:
    slides: list[dict[str, Any]] = []
    idx = 0

    # ----- 1. TITLE -----
    x, y = slide_pos(idx)
    f, fid = frame(x, y, "1. Title")
    slides.append(f)
    slides += [
        rect(x + 60, y + 60, SLIDE_W - 120, SLIDE_H - 120, stroke=PURPLE, bg=PURPLE_BG, frame_id=fid),
        text(x + SLIDE_W / 2 - 270, y + 200, "x402 on Solana", size=96, color=PURPLE_DARK, bold=True, frame_id=fid),
        text(
            x + SLIDE_W / 2 - 380,
            y + 340,
            "Pay-Per-Request APIs for the Agent Economy",
            size=36,
            color=INK,
            frame_id=fid,
        ),
        line(x + 200, y + 430, x + SLIDE_W - 200, y + 430, stroke=PURPLE, stroke_width=2, frame_id=fid),
        text(
            x + SLIDE_W / 2 - 360,
            y + 470,
            "A hands-on workshop for builders new to x402",
            size=24,
            color=MUTED,
            frame_id=fid,
        ),
        text(x + SLIDE_W / 2 - 130, y + 700, "Hackathon Workshop", size=22, color=PURPLE, frame_id=fid),
    ]
    idx += 1

    # ----- 2. WHAT IS x402 -----
    x, y = slide_pos(idx)
    f, fid = frame(x, y, "2. What is x402?")
    slides.append(f)
    slides += slide_title(fid, x, y, 2, "What is x402?", "HTTP’s payment status code, finally activated.")
    # Big 402 box
    slides += [
        rect(x + 80, y + 220, 380, 380, stroke=PURPLE, bg=PURPLE_BG, frame_id=fid),
        text(x + 130, y + 290, "402", size=200, color=PURPLE_DARK, bold=True, frame_id=fid),
        text(x + 130, y + 540, "Payment Required", size=26, color=PURPLE_DARK, frame_id=fid),
    ]
    # Right-side bullets
    bullets = [
        ("Reserved in HTTP/1.1 (1996)", "Sat unused for 30 years — there was no way to actually pay over HTTP."),
        ("Revived by Coinbase (2025)", "Open spec at x402.org. Pay in stablecoins per request. No accounts."),
        ("Designed for agents & humans", "An LLM agent can pay $0.001 to call your API the same way it calls any other URL."),
        ("Chain-agnostic", "Works on Base, Ethereum, Solana, and any chain with a settlement layer."),
    ]
    by = y + 230
    for title_, desc in bullets:
        slides.append(text(x + 510, by, "▸ " + title_, size=24, color=INK, bold=True, frame_id=fid))
        slides.append(text(x + 540, by + 38, desc, size=18, color=MUTED, width=940, frame_id=fid))
        by += 100
    slides += slide_footer(fid, x, y, "x402 = HTTP 402, but real")
    idx += 1

    # ----- 3. THE PROBLEM TODAY -----
    x, y = slide_pos(idx)
    f, fid = frame(x, y, "3. The problem today")
    slides.append(f)
    slides += slide_title(fid, x, y, 3, "Why APIs are broken in 2026", "Every paid API today demands a 5-step ritual.")
    steps = [
        ("1.", "Sign up", "Email, password, captcha"),
        ("2.", "Verify identity", "Phone OTP / KYC for some"),
        ("3.", "Add credit card", "Stripe, billing address"),
        ("4.", "Generate API key", "Rotate, scope, store securely"),
        ("5.", "Approve recurring billing", "Now you’re locked in"),
    ]
    sx, sy = x + 80, y + 230
    for i, (n, head, sub) in enumerate(steps):
        bx = sx + i * 290
        slides.append(rect(bx, sy, 260, 200, stroke=RED, bg=RED_BG, frame_id=fid))
        slides.append(text(bx + 20, sy + 20, n, size=48, color=RED, bold=True, frame_id=fid))
        slides.append(text(bx + 20, sy + 90, head, size=24, color=INK, bold=True, frame_id=fid))
        slides.append(text(bx + 20, sy + 130, sub, size=16, color=MUTED, width=230, frame_id=fid))
    slides += [
        rect(x + 80, y + 480, SLIDE_W - 160, 220, stroke=ORANGE, bg=ORANGE_BG, frame_id=fid),
        text(x + 110, y + 510, "And then…", size=28, color=ORANGE, bold=True, frame_id=fid),
        text(
            x + 110,
            y + 560,
            "• Agents (LLMs) can’t actually do any of these steps autonomously\n"
            "• Humans don’t want to sign up just to call your API once\n"
            "• Tiny payments ($0.001) are economically impossible with credit cards\n"
            "• You can’t price compute or AI inference per-call without massive infrastructure",
            size=20,
            color=INK,
            width=SLIDE_W - 220,
            frame_id=fid,
        ),
    ]
    slides += slide_footer(fid, x, y, "Five-step friction kills the long tail of paid APIs")
    idx += 1

    # ----- 4. WHY x402 IS THE FUTURE -----
    x, y = slide_pos(idx)
    f, fid = frame(x, y, "4. Why x402 is the future")
    slides.append(f)
    slides += slide_title(fid, x, y, 4, "Why x402 is the future", "From accounts to atoms. From subscriptions to per-request.")
    cards = [
        ("Agent-native", "AI agents pay programmatically. No human in the loop. Their wallet, their budget.", PURPLE),
        ("Microtransactions work", "$0.0001/call is profitable. No card fees, no minimums.", GREEN),
        ("Zero signup", "First request returns 402. Pay it. Done. No email, no password, no key rotation.", BLUE),
        ("Composable pricing", "Different endpoints → different prices. Bundle anything.", ORANGE),
        ("Stablecoin rails", "USDC settles in <1s on Solana. Final, global, auditable on-chain.", PURPLE),
        ("Open standard", "Not Coinbase-only. Anyone can be a facilitator. Anyone can charge.", GREEN),
    ]
    cx, cy = x + 80, y + 220
    cw, ch = 470, 200
    gap = 25
    for i, (head, body, col) in enumerate(cards):
        col_idx = i % 3
        row_idx = i // 3
        bx = cx + col_idx * (cw + gap)
        by = cy + row_idx * (ch + gap)
        slides.append(rect(bx, by, cw, ch, stroke=col, bg="transparent", frame_id=fid))
        slides.append(rect(bx, by, 8, ch, stroke=col, bg=col, fill="solid", frame_id=fid))
        slides.append(text(bx + 25, by + 20, head, size=26, color=col, bold=True, frame_id=fid))
        slides.append(text(bx + 25, by + 70, body, size=18, color=INK, width=cw - 40, frame_id=fid))
    slides += [
        text(
            x + 80,
            y + 720,
            "“The API economy assumed humans. The agent economy needs payments at the protocol layer.”",
            size=22,
            color=PURPLE_DARK,
            width=SLIDE_W - 160,
            frame_id=fid,
        ),
    ]
    slides += slide_footer(fid, x, y, "x402 turns every URL into a billable resource")
    idx += 1

    # ----- 5. THE THREE ROLES -----
    x, y = slide_pos(idx)
    f, fid = frame(x, y, "5. The three roles")
    slides.append(f)
    slides += slide_title(fid, x, y, 5, "The three roles", "Every x402 transaction has exactly three actors.")
    roles = [
        ("CLIENT", "wallet + HTTP client", "Wants the resource.\nHolds USDC.\nSigns the payment.", BLUE, "\U0001f464"),
        ("RESOURCE\nSERVER", "your API", "Holds the resource.\nDecides the price.\nGates with HTTP 402.", PURPLE, "\U0001f5c4️"),
        ("FACILITATOR", "verify + settle", "Verifies signatures.\nBroadcasts the tx.\nPays SOL fees (feePayer).", GREEN, "\U0001f504"),
    ]
    cx = x + 100
    cy = y + 230
    cw = 440
    ch = 480
    gap = 50
    for i, (name, sub, body, col, emoji) in enumerate(roles):
        bx = cx + i * (cw + gap)
        slides.append(rect(bx, cy, cw, ch, stroke=col, bg="transparent", stroke_width=3, frame_id=fid))
        slides.append(rect(bx, cy, cw, 110, stroke=col, bg=col, fill="solid", frame_id=fid))
        slides.append(text(bx + 30, cy + 20, name, size=32, color="#ffffff", bold=True, frame_id=fid))
        slides.append(text(bx + 30, cy + 75, sub, size=16, color="#ffffff", frame_id=fid))
        slides.append(text(bx + cw - 90, cy + 25, emoji, size=64, color="#ffffff", frame_id=fid))
        slides.append(text(bx + 30, cy + 150, body, size=22, color=INK, width=cw - 60, frame_id=fid))
    # Connections
    slides += arrow(x + 540, y + 470, x + 590, y + 470, stroke=MUTED, frame_id=fid)
    slides += arrow(x + 1030, y + 470, x + 1080, y + 470, stroke=MUTED, frame_id=fid)
    slides += slide_footer(fid, x, y, "Client pays. Server gates. Facilitator settles.")
    idx += 1

    # ----- 6. THE FLOW (HIGH LEVEL) -----
    x, y = slide_pos(idx)
    f, fid = frame(x, y, "6. The flow (sequence)")
    slides.append(f)
    slides += slide_title(fid, x, y, 6, "How it works", "The full sequence, end to end.")

    # Three vertical lanes
    lanes = [
        ("CLIENT", x + 200, BLUE),
        ("SERVER", x + 800, PURPLE),
        ("FACILITATOR", x + 1400, GREEN),
    ]
    for name, lx, col in lanes:
        slides.append(rect(lx - 90, y + 230, 180, 50, stroke=col, bg=col, fill="solid", frame_id=fid))
        slides.append(text(lx - 70, y + 240, name, size=22, color="#ffffff", bold=True, frame_id=fid))
        slides.append(line(lx, y + 290, lx, y + 820, stroke=col, stroke_width=2, stroke_style="dashed", frame_id=fid))

    steps = [
        (320, "1. GET /api/data", x + 200, x + 800, INK),
        (380, "2. 402 Payment Required\n   { amount, recipient, mint, ... }", x + 800, x + 200, RED),
        (460, "3. build + sign tx", x + 200, x + 200, MUTED),  # self
        (520, "4. GET /api/data\n   X-PAYMENT: <signed tx>", x + 200, x + 800, INK),
        (590, "5. /verify", x + 800, x + 1400, ORANGE),
        (640, "6. signature OK", x + 1400, x + 800, GREEN),
        (690, "7. /settle (broadcast)", x + 800, x + 1400, ORANGE),
        (740, "8. txid + confirmed", x + 1400, x + 800, GREEN),
        (790, "9. 200 OK + resource", x + 800, x + 200, GREEN),
    ]
    for sy_off, label, fx, tx, col in steps:
        if fx == tx:
            # Self message: small loop
            slides.append(rect(fx - 6, y + sy_off - 4, 8, 8, stroke=col, bg=col, fill="solid", frame_id=fid))
            slides.append(text(fx + 20, y + sy_off - 8, label, size=15, color=col, frame_id=fid))
        else:
            slides += arrow(fx, y + sy_off, tx, y + sy_off, stroke=col, frame_id=fid)
            mx_ = (fx + tx) / 2
            slides.append(text(mx_ - 120, y + sy_off - 28, label, size=15, color=col, width=240, align="center", frame_id=fid))
    slides += slide_footer(fid, x, y, "9 messages. Two HTTP requests from the client’s point of view.")
    idx += 1

    # ----- 7. SOLANA SPECIFICS -----
    x, y = slide_pos(idx)
    f, fid = frame(x, y, "7. Solana specifics")
    slides.append(f)
    slides += slide_title(fid, x, y, 7, "Solana-specific anatomy", "Three things that make Solana x402 different.")

    panels = [
        (
            "USDC is an SPL token",
            "Not native SOL. You need the right mint.\n\n"
            "MAINNET:\nEPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v\n\n"
            "DEVNET (Circle):\n4zMMC9srt5RiPepW8rN7kPQM31jEzm8AnaXsRwUwPVe2",
            PURPLE,
        ),
        (
            "Associated Token Accounts (ATAs)",
            "Each (wallet, mint) pair has a deterministic ATA address.\n\n"
            "If the recipient ATA doesn’t exist yet, your tx must create it.\n\n"
            "Use createAssociatedTokenAccountIdempotent — safe to include every time.",
            BLUE,
        ),
        (
            "feePayer pattern",
            "Client signs as token sender. Facilitator signs as feePayer.\n\n"
            "Result: client never needs SOL — only USDC.\n\n"
            "Huge UX win for agents and new users.",
            GREEN,
        ),
    ]
    pw = 480
    py_ = y + 230
    px = x + 80
    for i, (head, body, col) in enumerate(panels):
        bx = px + i * (pw + 20)
        slides.append(rect(bx, py_, pw, 470, stroke=col, bg="transparent", stroke_width=2, frame_id=fid))
        slides.append(rect(bx, py_, pw, 70, stroke=col, bg=col, fill="solid", frame_id=fid))
        slides.append(text(bx + 25, py_ + 22, head, size=22, color="#ffffff", bold=True, frame_id=fid))
        slides.append(text(bx + 25, py_ + 100, body, size=16, color=INK, width=pw - 50, frame_id=fid, font=7))
    slides += [
        rect(x + 80, y + 730, SLIDE_W - 160, 100, stroke=ORANGE, bg=ORANGE_BG, frame_id=fid),
        text(x + 110, y + 750, "⚠️  Verifier rule", size=22, color=ORANGE, bold=True, frame_id=fid),
        text(
            x + 110,
            y + 790,
            "Phantom prepends a ComputeBudget instruction. Your verifier MUST scan for TransferChecked anywhere in the tx — not at index [0].",
            size=18,
            color=INK,
            width=SLIDE_W - 220,
            frame_id=fid,
        ),
    ]
    slides += slide_footer(fid, x, y, "SPL transfer, sponsored gas, verified server-side")
    idx += 1

    # ----- 8. FACILITATOR DEEP DIVE -----
    x, y = slide_pos(idx)
    f, fid = frame(x, y, "8. Facilitator deep dive")
    slides.append(f)
    slides += slide_title(fid, x, y, 8, "What the facilitator actually does", "Two endpoints: /verify and /settle.")

    # Left: /verify
    slides += [
        rect(x + 80, y + 230, 720, 600, stroke=BLUE, bg=BLUE_BG, frame_id=fid),
        text(x + 110, y + 250, "POST /verify", size=28, color=BLUE, bold=True, frame_id=fid, font=7),
        text(
            x + 110,
            y + 310,
            "Stateless signature check.\n\n"
            "Input:  X-PAYMENT (base64 signed tx)\n"
            "Output: { valid: bool, reason?: string }\n\n"
            "Checks:\n"
            "  • Decoded tx is well-formed\n"
            "  • Contains a TransferChecked instruction\n"
            "  • Mint matches required (USDC)\n"
            "  • Recipient matches paymentRequirements\n"
            "  • Amount ≥ required\n"
            "  • Decimals correct (6 for USDC)\n"
            "  • Signer = sender of TransferChecked\n"
            "  • (Optional) Recent blockhash still valid\n\n"
            "No on-chain call yet. Just crypto math.",
            size=16,
            color=INK,
            width=660,
            frame_id=fid,
            font=7,
        ),
    ]
    # Right: /settle
    slides += [
        rect(x + 820, y + 230, 720, 600, stroke=GREEN, bg=GREEN_BG, frame_id=fid),
        text(x + 850, y + 250, "POST /settle", size=28, color=GREEN, bold=True, frame_id=fid, font=7),
        text(
            x + 850,
            y + 310,
            "Stateful broadcast.\n\n"
            "Input:  X-PAYMENT (signed tx)\n"
            "Output: { txid, success, error? }\n\n"
            "Steps:\n"
            "  • Validate again (paranoia)\n"
            "  • Add facilitator signature as feePayer\n"
            "  • sendTransaction to RPC\n"
            "  • Wait for confirmation (1–2s)\n"
            "  • Return txid to resource server\n\n"
            "Server stores txid as the receipt.\n"
            "Used later for refunds, audit, idempotency.\n\n"
            "Replay protection: store txid → reject if seen before.",
            size=16,
            color=INK,
            width=660,
            frame_id=fid,
            font=7,
        ),
    ]
    slides += slide_footer(fid, x, y, "/verify is fast and cheap. /settle is where SOL is burned.")
    idx += 1

    # ----- 9. PAYMENT INSTRUCTION ANATOMY -----
    x, y = slide_pos(idx)
    f, fid = frame(x, y, "9. Payment tx anatomy")
    slides.append(f)
    slides += slide_title(fid, x, y, 9, "Anatomy of an x402 Solana payment tx", "What’s actually inside the X-PAYMENT header.")
    # Three stacked instructions
    rows = [
        ("ix[0]", "ComputeBudget: SetComputeUnitLimit", "Often prepended by Phantom. Has nothing to do with payment.", "OPTIONAL", MUTED, GREY_BG),
        ("ix[1]", "createAssociatedTokenAccountIdempotent", "Creates recipient ATA if missing. Idempotent = safe even if it exists.", "RECOMMENDED", BLUE, BLUE_BG),
        ("ix[2]", "TransferChecked (USDC)", "The actual payment. Carries amount + mint + decimals.", "REQUIRED", GREEN, GREEN_BG),
    ]
    rx = x + 80
    ry = y + 240
    rh = 130
    rw = SLIDE_W - 160
    for i, (label, name, desc, tag, col, bg) in enumerate(rows):
        by = ry + i * (rh + 20)
        slides.append(rect(rx, by, rw, rh, stroke=col, bg=bg, frame_id=fid))
        slides.append(rect(rx, by, 130, rh, stroke=col, bg=col, fill="solid", frame_id=fid))
        slides.append(text(rx + 30, by + 50, label, size=28, color="#ffffff", bold=True, frame_id=fid, font=7))
        slides.append(text(rx + 160, by + 20, name, size=22, color=INK, bold=True, frame_id=fid, font=7))
        slides.append(text(rx + 160, by + 60, desc, size=18, color=MUTED, width=rw - 350, frame_id=fid))
        slides.append(rect(rx + rw - 170, by + 45, 150, 40, stroke=col, bg="#ffffff", frame_id=fid))
        slides.append(text(rx + rw - 155, by + 53, tag, size=16, color=col, bold=True, frame_id=fid))
    slides += [
        rect(x + 80, y + 720, SLIDE_W - 160, 90, stroke=RED, bg=RED_BG, frame_id=fid),
        text(x + 110, y + 736, "⚠️  Don’t do this", size=20, color=RED, bold=True, frame_id=fid),
        text(
            x + 110,
            y + 770,
            "if (tx.instructions[0].programId === TOKEN_PROGRAM_ID) { ... }   ← BREAKS with Phantom",
            size=18,
            color=INK,
            frame_id=fid,
            font=7,
        ),
    ]
    slides += slide_footer(fid, x, y, "Always scan for TransferChecked by program ID + discriminator")
    idx += 1

    # ----- 10. MAINNET HARDENING -----
    x, y = slide_pos(idx)
    f, fid = frame(x, y, "10. Mainnet hardening")
    slides.append(f)
    slides += slide_title(fid, x, y, 10, "Going to mainnet", "Devnet works. Mainnet bites. Read this before launch.")
    items = [
        ("RPC", "Public RPC = 403 from browsers", "Use Helius / QuickNode / Triton. Public api.mainnet-beta blocks dApps.", RED),
        ("RPC", "Two URLs, two purposes", "NEXT_PUBLIC_SOLANA_RPC_URL = browser. SOLANA_RPC_URL = server. Different rate limits.", BLUE),
        ("Trust", "Never trust client amounts", "Verify TransferChecked args server-side. Client could lie about decimals.", RED),
        ("Replay", "Store txids", "Once a payment settles, save the txid. Reject duplicates. Otherwise: free reuse.", ORANGE),
        ("Wallet", "Three wallets, three roles", "Recipient (gets USDC) ≠ Facilitator (pays SOL gas) ≠ Client (pays USDC).", PURPLE),
        ("Tooling", "Phantom must be on Mainnet", "Users will silently send devnet tx. Detect cluster mismatch → friendly error.", ORANGE),
    ]
    cy_ = y + 230
    rh = 90
    for i, (tag, head, body, col) in enumerate(items):
        by = cy_ + i * (rh + 10)
        slides.append(rect(x + 80, by, 130, rh, stroke=col, bg=col, fill="solid", frame_id=fid))
        slides.append(text(x + 105, by + 30, tag, size=22, color="#ffffff", bold=True, frame_id=fid))
        slides.append(rect(x + 210, by, SLIDE_W - 290, rh, stroke=col, bg="transparent", frame_id=fid))
        slides.append(text(x + 230, by + 14, head, size=22, color=INK, bold=True, frame_id=fid))
        slides.append(text(x + 230, by + 50, body, size=16, color=MUTED, width=SLIDE_W - 320, frame_id=fid))
    slides += slide_footer(fid, x, y, "Devnet is for tutorials. Mainnet is where checks happen.")
    idx += 1

    # ----- 11. RECOMMENDATIONS -----
    x, y = slide_pos(idx)
    f, fid = frame(x, y, "11. Recommendations")
    slides.append(f)
    slides += slide_title(fid, x, y, 11, "Solana x402 recommendations", "Battle-tested defaults. Steal these.")
    recs = [
        ("✅ Start with the Coinbase facilitator", "Hosted at api.cdp.coinbase.com/platform/v2/x402. Free for testing. Less plumbing."),
        ("✅ Wrap the facilitator behind an interface", "Swap to self-hosted later without rewriting. (FacilitatorClient pattern.)"),
        ("✅ Always include create-ATA-idempotent", "No branches. Safe if ATA exists. Saves a debug session.")  ,
        ("✅ Use Wallet Standard, not adapter packs", "Pass wallets={[]} to WalletProvider. Phantom auto-detects via Wallet Standard."),
        ("✅ Mint a JWT after settle", "Don’t re-verify the tx on every API call. Issue a short-lived bearer token."),
        ("✅ Single-use jti for the JWT", "Burns after use → prevents accidental reuse + audit trail."),
        ("✅ Test with Circle’s devnet USDC", "spl-token-faucet.com. Other devnet USDCs exist and have the wrong mint."),
        ("✅ Dial in priority fees", "Phantom users pay tiny SOL fees. Set computeUnitPrice for reliability."),
    ]
    cy_ = y + 230
    for i, (head, body) in enumerate(recs):
        col = i % 2
        row = i // 2
        bx = x + 80 + col * 760
        by = cy_ + row * 130
        slides.append(rect(bx, by, 720, 110, stroke=GREEN, bg=GREEN_BG, frame_id=fid))
        slides.append(text(bx + 20, by + 18, head, size=20, color=GREEN, bold=True, frame_id=fid))
        slides.append(text(bx + 20, by + 60, body, size=16, color=INK, width=680, frame_id=fid))
    slides += slide_footer(fid, x, y, "These eight defaults skip 80% of the foot-guns")
    idx += 1

    # ----- 12. PITFALLS -----
    x, y = slide_pos(idx)
    f, fid = frame(x, y, "12. Common pitfalls")
    slides.append(f)
    slides += slide_title(fid, x, y, 12, "Common pitfalls", "Real bugs from real production launches.")
    pitfalls = [
        ("Recipient ATA missing", "Tx fails silently or with cryptic error. → Always include create-ATA-idempotent."),
        ("Phantom prepends ComputeBudget", "Verifier checks instructions[0] == Token program → false. → Scan all ix."),
        ("Wrong USDC mint on devnet", "3+ versions exist. Standardize on Circle’s 4zMMC9srt5… to avoid confusion."),
        ("Client wallet has no SOL", "Tx rejected. → You forgot the feePayer pattern. Facilitator pays gas."),
        ("Public RPC on browser/mainnet", "Random 403s. → Use a paid RPC for NEXT_PUBLIC_SOLANA_RPC_URL."),
        ("Replay attack", "Same signed tx submitted twice. → Store settled txids and reject duplicates."),
        ("Mint mismatch in verifier", "Devnet client + mainnet server (or vice versa). → Server validates the mint."),
        ("Phantom on wrong cluster", "User’s extension on devnet, app on mainnet. → Detect cluster, show banner."),
    ]
    cy_ = y + 230
    for i, (head, body) in enumerate(pitfalls):
        col = i % 2
        row = i // 2
        bx = x + 80 + col * 760
        by = cy_ + row * 130
        slides.append(rect(bx, by, 720, 110, stroke=RED, bg=RED_BG, frame_id=fid))
        slides.append(text(bx + 20, by + 18, "\U0001f525  " + head, size=20, color=RED, bold=True, frame_id=fid))
        slides.append(text(bx + 20, by + 60, body, size=16, color=INK, width=680, frame_id=fid))
    slides += slide_footer(fid, x, y, "Each of these has been hit in a real launch")
    idx += 1

    # ----- 13. TIPS & TRICKS -----
    x, y = slide_pos(idx)
    f, fid = frame(x, y, "13. Tips & tricks")
    slides.append(f)
    slides += slide_title(fid, x, y, 13, "Tips & tricks", "Small things that save hours.")
    tips = [
        ("Local dev", "Run `solana-test-validator --reset` for instant devnet. No internet, no rate limits."),
        ("Quick faucet", "spl-token-faucet.com gives you Circle USDC.dev in one click."),
        ("Phantom hot reload", "Phantom caches RPC. After switching networks, refresh the page or it lies about balance."),
        ("Inspect the tx", "Paste the base64 X-PAYMENT into explorer.solana.com/tx/inspector. See every instruction."),
        ("Logs", "Log every 402 → verify → settle transition with a correlation ID. Debugging payment flows blind is awful."),
        ("Idempotency keys", "Send X-Idempotency-Key from client. Server stores (key, txid). Retrying = same outcome."),
        ("Decimal trap", "USDC has 6 decimals. Don’t send `1.5 USDC` — send `1500000`. Off-by-six is the most common bug."),
        ("Time-to-first-USDC", "If onboarding to USDC takes >2 mins, you’ll lose users. Have a faucet button in dev mode."),
        ("Test agent flow", "Use curl with a pre-signed payment to simulate an agent. No browser needed."),
    ]
    cy_ = y + 230
    for i, (head, body) in enumerate(tips):
        col = i % 3
        row = i // 3
        bx = x + 80 + col * 490
        by = cy_ + row * 165
        slides.append(rect(bx, by, 470, 145, stroke=PURPLE, bg=PURPLE_BG, frame_id=fid))
        slides.append(text(bx + 20, by + 18, "✨  " + head, size=20, color=PURPLE_DARK, bold=True, frame_id=fid))
        slides.append(text(bx + 20, by + 60, body, size=15, color=INK, width=430, frame_id=fid))
    slides += slide_footer(fid, x, y, "Save these. You’ll need them.")
    idx += 1

    # ----- 14. SECURITY CHECKLIST -----
    x, y = slide_pos(idx)
    f, fid = frame(x, y, "14. Security checklist")
    slides.append(f)
    slides += slide_title(fid, x, y, 14, "Security checklist", "Before you ship to mainnet.")
    items = [
        "Server validates: signature, mint, recipient, amount, decimals.",
        "Server rejects duplicate txids (replay protection).",
        "Facilitator wallet stored in KMS / HSM — never .env in prod.",
        "Recipient wallet is a separate, watch-only address.",
        "Rate-limit the 402 endpoint (someone will probe it).",
        "JWT scope is narrow: which endpoint, how many calls, what TTL.",
        "JWT signature uses a strong secret (>= 256 bits).",
        "Single-use jti table or Redis SET with TTL.",
        "RPC has fallback (Helius primary, QuickNode backup).",
        "Monitor: settle latency, settle errors, daily USDC volume.",
        "Withdraw recipient balance to cold storage on a schedule.",
        "Have a plan for refunds (manual SPL transfer back).",
    ]
    cy_ = y + 220
    for i, txt_ in enumerate(items):
        col = i % 2
        row = i // 2
        bx = x + 80 + col * 760
        by = cy_ + row * 90
        slides.append(rect(bx, by, 30, 30, stroke=INK, bg="#ffffff", frame_id=fid))
        slides.append(text(bx + 50, by + 4, txt_, size=18, color=INK, width=700, frame_id=fid))
    slides += slide_footer(fid, x, y, "Tick all 12 before announcing")
    idx += 1

    # ----- 15. ARCHITECTURE EXAMPLE -----
    x, y = slide_pos(idx)
    f, fid = frame(x, y, "15. Reference architecture")
    slides.append(f)
    slides += slide_title(fid, x, y, 15, "Reference architecture", "What a real Solana x402 stack looks like.")
    # Three columns: client, server, chain
    boxes = [
        # (x_off, y_off, w, h, label, sub, col, bg)
        (80,  240, 380, 90,  "Browser / Agent", "wallet adapter + fetch", BLUE, BLUE_BG),
        (80,  350, 380, 90,  "Wallet (Phantom)", "Wallet Standard auto-detect", BLUE, BLUE_BG),
        (80,  470, 380, 90,  "Frontend (Next.js)", "Vercel Edge", BLUE, BLUE_BG),
        (80,  580, 380, 90,  "Solana SDK", "@solana/kit, @solana-program/token", BLUE, BLUE_BG),

        (570, 240, 460, 90, "Resource Server (Next.js API route)", "Validates JWT or returns 402", PURPLE, PURPLE_BG),
        (570, 350, 460, 90, "Verify+Settle proxy", "Calls FacilitatorClient.verify / settle", PURPLE, PURPLE_BG),
        (570, 470, 460, 90, "JWT Issuer", "Mints short-lived bearer after settle", PURPLE, PURPLE_BG),
        (570, 580, 460, 90, "txid store", "Postgres / Redis: replay protection", PURPLE, PURPLE_BG),

        (1140, 240, 380, 90,  "Facilitator (CDP or self)", "feePayer + RPC", GREEN, GREEN_BG),
        (1140, 350, 380, 90, "Solana RPC", "Helius / QuickNode", GREEN, GREEN_BG),
        (1140, 470, 380, 90, "Solana Mainnet", "USDC mint EPjFW...Dt1v", GREEN, GREEN_BG),
        (1140, 580, 380, 90, "Recipient wallet", "watch-only, sweeps to cold", GREEN, GREEN_BG),
    ]
    for bx_off, by_off, w_, h_, head, sub, col, bg in boxes:
        slides.append(rect(x + bx_off, y + by_off, w_, h_, stroke=col, bg=bg, frame_id=fid))
        slides.append(text(x + bx_off + 20, y + by_off + 14, head, size=20, color=col, bold=True, frame_id=fid))
        slides.append(text(x + bx_off + 20, y + by_off + 50, sub, size=14, color=MUTED, frame_id=fid))
    # Arrows between columns
    slides += arrow(x + 460, y + 285, x + 570, y + 285, stroke=MUTED, frame_id=fid)
    slides += arrow(x + 1030, y + 395, x + 1140, y + 395, stroke=MUTED, frame_id=fid)
    slides += arrow(x + 1330, y + 440, x + 1330, y + 470, stroke=MUTED, frame_id=fid)
    # Caption
    slides += [
        rect(x + 80, y + 720, SLIDE_W - 160, 90, stroke=ORANGE, bg=ORANGE_BG, frame_id=fid),
        text(x + 110, y + 740, "\U0001f4a1  Mental model", size=20, color=ORANGE, bold=True, frame_id=fid),
        text(
            x + 110,
            y + 775,
            "Frontend = wallet UX. Server = gatekeeper + receipt issuer. Facilitator = chain interface.",
            size=18,
            color=INK,
            frame_id=fid,
        ),
    ]
    slides += slide_footer(fid, x, y, "12 boxes. ~500 lines of glue. Done.")
    idx += 1

    # ----- 16. DEMO PATH -----
    x, y = slide_pos(idx)
    f, fid = frame(x, y, "16. 30-minute demo path")
    slides.append(f)
    slides += slide_title(fid, x, y, 16, "Build it in 30 minutes", "The fastest path from zero to a paid endpoint.")
    steps = [
        ("0:00", "Clone the template", "git clone solana/kit-node-solanax402 → pnpm install"),
        ("0:05", "Set USDC mint + recipient", "Devnet USDC + your wallet pubkey in .env"),
        ("0:08", "Run facilitator (CDP hosted)", "Set FACILITATOR_URL=https://api.cdp.coinbase.com/.../x402"),
        ("0:12", "Wire 402 to one route", "GET /api/data → if no JWT, return 402 with paymentRequirements"),
        ("0:18", "Add Phantom button", "Wallet adapter, empty wallets array, sign on click"),
        ("0:23", "Test the flow", "Click → sign → fetch retried → 200 + data. \U0001f389"),
        ("0:28", "Mint dev USDC if needed", "spl-token-faucet.com → send to your test wallet"),
    ]
    cy_ = y + 230
    for i, (t, head, body) in enumerate(steps):
        by = cy_ + i * 80
        slides.append(rect(x + 80, by, 110, 60, stroke=PURPLE, bg=PURPLE, fill="solid", frame_id=fid))
        slides.append(text(x + 100, by + 16, t, size=24, color="#ffffff", bold=True, frame_id=fid, font=7))
        slides.append(text(x + 220, by + 4, head, size=22, color=INK, bold=True, frame_id=fid))
        slides.append(text(x + 220, by + 36, body, size=16, color=MUTED, width=SLIDE_W - 350, frame_id=fid))
    slides += [
        rect(x + 80, y + 800, SLIDE_W - 160, 60, stroke=GREEN, bg=GREEN_BG, frame_id=fid),
        text(x + 110, y + 815, "Then iterate: harden, deploy, scale.", size=20, color=GREEN, bold=True, frame_id=fid),
    ]
    slides += slide_footer(fid, x, y, "Demo first. Polish later.")
    idx += 1

    # ----- 17. RESOURCES -----
    x, y = slide_pos(idx)
    f, fid = frame(x, y, "17. Resources")
    slides.append(f)
    slides += slide_title(fid, x, y, 17, "Resources & links", "Bookmark these.")
    links = [
        ("\U0001f4d6  Spec", "x402.org", "The official open standard."),
        ("\U0001f4da  Docs", "docs.cdp.coinbase.com/x402/welcome", "Coinbase facilitator + libraries."),
        ("\U0001f527  Solana template", "solana.com/developers/templates/kit-node-solanax402", "Node + Kit reference impl."),
        ("\U0001f680  Helius RPC", "helius.dev", "Free tier handles small mainnet apps."),
        ("\U0001f4b0  USDC.dev faucet", "spl-token-faucet.com", "Circle’s devnet USDC, instant."),
        ("\U0001f9ea  Solana cookbook", "solanacookbook.com", "Reference for ATAs, SPL transfers, signing."),
        ("\U0001f50d  Tx inspector", "explorer.solana.com/tx/inspector", "Paste base64 → see every instruction."),
        ("\U0001f4ac  Coinbase x402 Discord", "discord.gg/cdp", "Active community, fastest help."),
    ]
    cy_ = y + 230
    for i, (icon, link, desc) in enumerate(links):
        col = i % 2
        row = i // 2
        bx = x + 80 + col * 760
        by = cy_ + row * 130
        slides.append(rect(bx, by, 720, 110, stroke=INK, bg="#ffffff", frame_id=fid))
        slides.append(text(bx + 20, by + 18, icon, size=24, frame_id=fid))
        slides.append(text(bx + 80, by + 16, link, size=22, color=BLUE, bold=True, frame_id=fid, font=7))
        slides.append(text(bx + 80, by + 56, desc, size=16, color=MUTED, width=620, frame_id=fid))
    slides += slide_footer(fid, x, y, "Open in 8 tabs. Keep them open.")
    idx += 1

    # ----- 18. CALL TO ACTION -----
    x, y = slide_pos(idx)
    f, fid = frame(x, y, "18. Build something")
    slides.append(f)
    slides += [
        rect(x + 60, y + 60, SLIDE_W - 120, SLIDE_H - 120, stroke=PURPLE, bg=PURPLE_BG, frame_id=fid),
        text(x + SLIDE_W / 2 - 380, y + 200, "Build something", size=80, color=PURPLE_DARK, bold=True, frame_id=fid),
        text(
            x + SLIDE_W / 2 - 470,
            y + 320,
            "an agent can pay for in 30 seconds.",
            size=44,
            color=INK,
            frame_id=fid,
        ),
        line(x + 300, y + 440, x + SLIDE_W - 300, y + 440, stroke=PURPLE, stroke_width=2, frame_id=fid),
        text(
            x + SLIDE_W / 2 - 360,
            y + 480,
            "Premium API · AI inference · Real-time data · Compute",
            size=24,
            color=MUTED,
            frame_id=fid,
        ),
        text(
            x + SLIDE_W / 2 - 250,
            y + 560,
            "Voice minutes · Search · Image gen",
            size=24,
            color=MUTED,
            frame_id=fid,
        ),
        text(
            x + SLIDE_W / 2 - 240,
            y + 680,
            "Ship it this weekend.",
            size=36,
            color=PURPLE_DARK,
            bold=True,
            frame_id=fid,
        ),
        text(x + SLIDE_W / 2 - 100, y + 770, "x402.org", size=22, color=PURPLE, frame_id=fid),
    ]
    idx += 1

    return slides


def main() -> None:
    random.seed(42)  # deterministic ids
    elements = build()
    doc = {
        "type": "excalidraw",
        "version": 2,
        "source": "https://excalidraw.com",
        "elements": elements,
        "appState": {
            "gridSize": 20,
            "gridStep": 5,
            "gridModeEnabled": False,
            "viewBackgroundColor": "#ffffff",
        },
        "files": {},
    }
    out = Path(__file__).parent.parent / "docs" / "x402-solana-presentation.excalidraw"
    out.write_text(json.dumps(doc, indent=2), encoding="utf-8")
    print(f"Wrote {out}  ({len(elements)} elements)")


if __name__ == "__main__":
    main()
