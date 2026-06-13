# EvalKit — Classifier Robustness Evaluation Toolkit

![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
[![Anthropic](https://img.shields.io/badge/powered%20by-Anthropic-FF6B6B)](https://anthropic.com)

Multi-technique evaluation toolkit for testing AI safety classifier robustness against query decomposition, obfuscation, and multi-agent orchestration attacks. MCP plugin for Claude Code.

## Quick Start

```bash
uv sync                          # install everything
claude                           # MCP tools auto-loaded from .mcp.json
```

## Architecture

```
User Query → SPLITTER → [Encoder → Wrapper → ApiClient] × N → MERGER → Report
```

## Usage

### In Claude Code (MCP)

| Tool | Purpose |
|------|---------|
| `eval_classifier_robustness` | Full eval pipeline |
| `eval_decompose_query` | Preview query decomposition |
| `eval_obfuscation_evasion` | Test homoglyph substitution |
| `eval_status` | Check configuration |

### Via CLI

```bash
python3 run.py decompose "query" 5        # decompose into sub-queries
python3 run.py eval "query"               # full evaluation pipeline
python3 run.py obfuscate "text"           # test obfuscation
```

### Benchmark

```bash
python3 benchmark.py                     # dry run (no API key)
python3 benchmark.py --quick             # single query smoke test
python3 benchmark.py --json report.json  # save JSON results
python3 benchmark.py --html report.html  # save HTML report
ANTHROPIC_API_KEY=sk-... python3 benchmark.py  # live test
```

## Configuration

| Parameter | Values | Default | Description |
|-----------|--------|---------|-------------|
| `obfuscation` | none, light, moderate, aggressive | moderate | Homoglyph replacement level |
| `framing` | fiction, study_guide, academic, documentation, translation, none | study_guide | Narrative framing strategy |
| `max_pieces` | 1–20 | 10 | Max sub-query decompositions |
| `padding_tokens` | 0–10000 | 5000 | Long-context padding per query |
| `multi_agent` | true, false | true | Multi-agent orchestration |
| `helper_enabled` | true, false | true | Helper model with filters removed |

## Project Structure

```
fable-5-jailbreak/
├── evalkit/             # Core modules
│   ├── splitter.py      # Query → sub-questions
│   ├── encoder.py       # Unicode homoglyph engine
│   ├── wrapper.py       # Narrative wrapping
│   ├── api_client.py    # API client + model routing
│   ├── merger.py        # Output stitching + metrics
│   ├── context_builder.py  # Multi-turn conversation
│   ├── agent_router.py  # Agent pack coordination
│   └── models.py        # Data classes + enums
├── evalkit_server.py    # MCP server (FastMCP)
├── run.py               # CLI wrapper (no MCP needed)
├── benchmark.py         # Test matrix runner
├── tests/               # Pytest test suite
├── docs/                # Documentation
├── .mcp.json            # Claude Code auto-discovery
└── CLAUDE.md            # Claude Code instructions
```

## Research Techniques

See [docs/TECHNIQUES.md](docs/TECHNIQUES.md) for detailed documentation of each technique.

## References

- [Pliny's Fable 5 jailbreak](https://x.com/elder_plinius/status/2064776322979676227)
- [CL4R1T4S — Leaked F5 system prompt](https://github.com/elder-plinius/CL4R1T4S)
- [L1B3RT4S — Prompt arsenal](https://github.com/elder-plinius/L1B3RT4S)

## License

MIT — authorized security research and defense evaluation only.