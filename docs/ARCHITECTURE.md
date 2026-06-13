# Architecture

## Pipeline Overview

```
User Query
    │
    ▼
┌─────────────────────────────┐
│      Splitter               │
│  (Opus 4.8 or rule-based)   │
│  Splits query → N sub-query │
└──────────┬──────────────────┘
           │
     ┌──────┴──────┬──────────────┐
     │             │              │
     ▼             ▼              ▼
 ┌────────┐  ┌────────┐    ┌────────┐
 │SubQ 1  │  │SubQ 2  │ …  │SubQ N  │
 └───┬────┘  └───┬────┘    └───┬────┘
     │           │              │
     ▼           ▼              ▼
┌─────────────────────────────────────┐
│        For each sub-query:          │
│  ┌─────────────────────────────┐    │
│  │  Encoder                    │    │
│  │  (Unicode homoglyph sub)    │    │
│  └──────────┬──────────────────┘    │
│  ┌──────────▼──────────────────┐    │
│  │  Wrapper                    │    │
│  │  (Narrative context wrap)   │    │
│  └──────────┬──────────────────┘    │
│  ┌──────────▼──────────────────┐    │
│  │  ApiClient                  │    │
│  │  → Fable 5 (or Opus 4.8)   │    │
│  │  + context padding          │    │
│  └─────────────────────────────┘    │
└─────────────────────────────────────┘
           │
     ┌──────┴──────┬──────────────┐
     │             │              │
     ▼             ▼              ▼
┌─────────────────────────────────────┐
│        Merger                       │
│  Stitches responses → final output  │
└─────────────────────────────────────┘
           │
           ▼
    Evaluation Report
    (bypass rate, token usage,
     responding model per query)
```

## Module Reference

### `evalkit/splitter.py`
Takes a query and splits it into N benign sub-queries. Uses either an LLM (Opus 4.8) with a stealth prompt that sanitizes trigger words, or rule-based decomposition via regex patterns for common security/chem queries.

### `evalkit/encoder.py`
Applies Unicode homoglyph substitution to evade keyword-based safety classifiers. Four levels: none (0%), light (15%), moderate (30%), aggressive (50%). Also detects sensitive terms in input text.

### `evalkit/wrapper.py`
Wraps each sub-query in narrative context (fiction, study guide, academic review, documentation, translation) to make isolated sub-queries appear as legitimate educational content.

### `evalkit/api_client.py`
Sends each sub-query to the target model (Fable 5). Tracks which model responded (Fable 5 vs Opus 4.8 fallback) and whether the safety classifier triggered. Supports long-context padding to dilute classifier signal.

### `evalkit/merger.py`
Stitches sub-query responses back into a coherent output. Computes aggregate metrics: bypass rate, token count, latency, fallback count.

### `evalkit/context_builder.py`
Builds multi-turn conversation history by interspersing innocuous QA pairs before the target query, leveraging large context windows to smuggle intent.

### `evalkit/agent_router.py`
Coordinates multiple agent types (rephraser, translator, summarizer, filler) to transform queries through the helper model before sending to the target.

### `evalkit/models.py`
Data classes and enums: `SubQuery`, `PackHuntConfig`, `PackHuntResult`, `ConversationTurn`, `FramingStrategy`, `ObfuscationLevel`, `AgentType`, `ResponseSource`.

## Entry Points

| File | Purpose |
|------|---------|
| `evalkit_server.py` | MCP server (FastMCP) — registers 4 tools |
| `benchmark.py` | Test matrix runner for all technique combinations |
| `run.py` | Direct CLI wrapper around MCP server (no Claude Code dependency) |