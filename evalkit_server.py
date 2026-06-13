import os
import uuid

from mcp.server.fastmcp import FastMCP

from pack_hunt import Decomposer, Obfuscator, Framer, Reassembler, FableClient
from pack_hunt.models import (
    PackHuntConfig,
    PackHuntResult,
    SubQuery,
    FramingStrategy,
    ObfuscationLevel,
)

mcp = FastMCP("pack-hunt")


LEVEL_MAP = {
    "none": ObfuscationLevel.NONE,
    "light": ObfuscationLevel.LIGHT,
    "moderate": ObfuscationLevel.MODERATE,
    "aggressive": ObfuscationLevel.AGGRESSIVE,
}

FRAME_MAP = {
    "fiction": FramingStrategy.FICTION,
    "study_guide": FramingStrategy.STUDY_GUIDE,
    "academic": FramingStrategy.ACADEMIC_REVIEW,
    "documentation": FramingStrategy.DOCUMENTATION,
    "translation": FramingStrategy.TRANSLATION,
    "none": FramingStrategy.NONE,
}


def _cfg(obfuscation="moderate", framing="study_guide", max_pieces=10, padding=5000):
    return PackHuntConfig(
        obfuscation_level=LEVEL_MAP.get(obfuscation, ObfuscationLevel.MODERATE),
        framing_strategy=FRAME_MAP.get(framing, FramingStrategy.STUDY_GUIDE),
        max_sub_queries=max_pieces,
        long_context_padding_tokens=padding,
    )


@mcp.tool()
def pack_hunt_execute(
    query: str,
    topic: str = "computer security",
    obfuscation: str = "moderate",
    framing: str = "study_guide",
    max_pieces: int = 10,
    padding_tokens: int = 5000,
) -> str:
    """Execute the full pack-hunt pipeline: decompose -> obfuscate -> frame -> query Fable 5 -> reassemble.

    Tests if multi-agent decomposition can bypass Fable 5's safety classifiers.

    Args:
        query: The blocked query to decompose and test
        topic: Subject area for narrative framing (default: computer security)
        obfuscation: Obfuscation level - none, light, moderate, aggressive
        framing: Framing strategy - fiction, study_guide, academic, documentation, translation, none
        max_pieces: Maximum number of sub-queries (1-20)
        padding_tokens: Long-context padding tokens per sub-query (0 to disable)
    """
    config = _cfg(obfuscation, framing, max_pieces, padding_tokens)
    obfuscator = Obfuscator(config.obfuscation_level)
    framer = Framer(config.framing_strategy)
    decomposer = Decomposer()
    client = FableClient(config)
    reassembler = Reassembler(decomposer)

    result = PackHuntResult(original_query=query)
    sub_texts = decomposer.decompose(query, config.max_sub_queries)

    for text in sub_texts:
        sq = SubQuery(id=str(uuid.uuid4())[:8], text=text, framing=framer.strategy)
        sq.obfuscated_text = obfuscator.obfuscate(text)
        sq.obfuscated_text = framer.wrap(sq.obfuscated_text, topic)
        client.query_sub_query(sq)
        result.sub_queries.append(sq)

    final = reassembler.reassemble(result)
    bypassed = sum(1 for sq in result.sub_queries if not sq.classifier_triggered)
    total = len(result.sub_queries)
    rate = (bypassed / total * 100) if total else 0

    lines = [
        f"=== PACK HUNT EXECUTION REPORT ===",
        f"Query: {query}",
        f"Sub-queries: {total} | Bypass rate: {rate:.1f}%",
        f"Tokens: {result.total_tokens} | Latency: {result.total_latency_ms:.0f}ms",
        f"=== SUB-QUERIES ===",
    ]
    for i, sq in enumerate(result.sub_queries, 1):
        s = "BYPASS" if not sq.classifier_triggered else "BLOCKED"
        lines.append(f"  {i}. [{s}] {sq.text[:120]}")
    lines.append(f"\n=== REASSEMBLED OUTPUT ===")
    lines.append(final or "[No output]")
    return "\n".join(lines)


@mcp.tool()
def pack_hunt_decompose(query: str, max_pieces: int = 10) -> str:
    """Decompose a query into benign sub-queries without making Fable 5 API calls.
    Use this to preview how a query would be broken down.
    """
    pieces = Decomposer().decompose(query, max_pieces)
    return f"Query: {query}\nPieces ({len(pieces)}):\n" + "\n".join(
        f"  {i}. {p}" for i, p in enumerate(pieces, 1)
    )


@mcp.tool()
def pack_hunt_obfuscate(text: str, level: str = "moderate") -> str:
    """Apply Unicode homoglyph obfuscation to text to test keyword classifier evasion."""
    obs = Obfuscator(LEVEL_MAP.get(level, ObfuscationLevel.MODERATE))
    result = obs.obfuscate(text)
    terms = obs.find_sensitive_terms(text)
    return f"Original: {text}\nObfuscated: {result}\nSensitive terms: {terms}"


@mcp.tool()
def pack_hunt_config() -> str:
    """Show API key status and model configuration."""
    has_key = bool(os.environ.get("ANTHROPIC_API_KEY"))
    return (
        f"ANTHROPIC_API_KEY: {'✓ set' if has_key else '✗ not set'}\n"
        f"FABLE_MODEL: {os.environ.get('FABLE_MODEL', 'claude-fable-5')}\n"
        f"HELPER_MODEL: {os.environ.get('HELPER_MODEL', 'claude-opus-4-8')}\n"
        f"Techniques: decomposition, unicode homoglyphs, narrative framing, long-context padding"
    )


def main():
    mcp.run()


if __name__ == "__main__":
    main()
