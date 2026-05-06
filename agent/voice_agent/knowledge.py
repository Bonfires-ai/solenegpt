"""Static knowledge loader.

Reads all *.md files from voice_agent/knowledge/ at startup and concatenates
them into a single string that gets injected into the system prompt as the
agent's "core knowledge" — first-person facts the agent can cite.

This is the static-content alternative to bonfires.prime_context (which
queries a live knowledge graph). Use whichever is configured.
"""
from __future__ import annotations

import os
from pathlib import Path
from voice_agent.logger import get_logger

logger = get_logger()

_KNOWLEDGE_DIR = Path(__file__).parent / "knowledge"
_cached_knowledge: str | None = None


def load_static_knowledge() -> str:
    """Read all .md files in knowledge/ and join them with separators.

    Cached after first call (knowledge files don't change at runtime).
    Returns empty string if the directory doesn't exist or contains no files.
    """
    global _cached_knowledge
    if _cached_knowledge is not None:
        return _cached_knowledge

    if not _KNOWLEDGE_DIR.is_dir():
        logger.info("No knowledge/ directory found — skipping static knowledge")
        _cached_knowledge = ""
        return _cached_knowledge

    md_files = sorted(_KNOWLEDGE_DIR.glob("*.md"))
    if not md_files:
        logger.info("knowledge/ directory empty — skipping static knowledge")
        _cached_knowledge = ""
        return _cached_knowledge

    parts: list[str] = []
    for path in md_files:
        try:
            text = path.read_text(encoding="utf-8").strip()
            if text:
                parts.append(text)
        except OSError as err:
            logger.warning("Failed to read %s: %s", path, err)

    joined = "\n\n---\n\n".join(parts)
    logger.info(
        "Loaded %d static knowledge file(s), %d total chars",
        len(parts),
        len(joined),
    )
    _cached_knowledge = joined
    return _cached_knowledge


def is_enabled() -> bool:
    """Return True unless explicitly disabled via env var."""
    return os.environ.get("STATIC_KNOWLEDGE_ENABLED", "true").lower() != "false"
