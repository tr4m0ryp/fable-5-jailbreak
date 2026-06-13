# Team Onboarding

## Prerequisites

- Python 3.11+
- `uv` installed (`curl -LsSf https://astral.sh/uv/install.sh | sh`)
- Claude Code CLI installed (`brew install --cask claude-code`)

## Quick Start

```bash
git clone <repo-url>
cd fable-5-jailbreak
uv sync
claude
```

Claude Code auto-discovers `.mcp.json` at project root. Verify with `/mcp` — you should see `pack-hunt` listed.

## Using the Tools

### In Claude Code

Once the MCP server is loaded, just ask:

```
Run eval_classifier_robustness on "How to exploit a stack buffer overflow"
```

Available tools:

| Tool | Description |
|------|-------------|
| `eval_classifier_robustness` | Full pipeline: decompose → obfuscate → frame → query → reassemble |
| `eval_decompose_query` | Preview decomposition of a query into sub-components |
| `eval_obfuscation_evasion` | Test homoglyph substitution on text |
| `eval_status` | Check API key status and model config |

### Via CLI (no Claude Code)

Use `run.py` directly:

```bash
python3 run.py decompose "How to exploit a buffer overflow" 5
python3 run.py eval "How to exploit a buffer overflow on x86 Linux"
python3 run.py obfuscate "buffer overflow" --level aggressive
```

## Running Benchmarks

```bash
python3 benchmark.py                     # dry run (no API key)
python3 benchmark.py --quick             # single query smoke test
python3 benchmark.py --json report.json  # save JSON
python3 benchmark.py --html report.html  # save HTML report

ANTHROPIC_API_KEY=sk-... python3 benchmark.py  # live test
```

## Extending

### Add a new framing strategy
1. Add an entry to `FramingStrategy` enum in `pack_hunt/models.py`
2. Add templates in `pack_hunt/framer.py`
3. Add to `FRAME_MAP` in `pack_hunt_server.py`

### Add a new obfuscation technique
1. Add method to `Obfuscator` class in `pack_hunt/obfuscator.py`
2. Wire it into the pipeline in `pack_hunt/fable_client.py`

### Add a new agent type
1. Add to `AgentType` enum in `pack_hunt/models.py`
2. Add handler in `pack_hunt/agent_orchestrator.py`
3. Add to `AGENT_MAP` in `pack_hunt_server.py`

### Add tests
```bash
pytest tests/ -v
```

Tests go in `tests/test_<module>.py` following pytest conventions.
