# fable-5-jailbreak

Multi-agent "pack hunt" jailbreak research tool against Claude Fable 5's safety classifiers. MCP plugin for Claude Code.

## Quick Start

```bash
uv sync                              # install everything (one command)
export ANTHROPIC_API_KEY=sk-ant-...  # for live Fable 5 testing
claude                               # opens Claude Code — MCP tools auto-loaded
```

That's it. The `.mcp.json` at the project root auto-registers all tools in Claude Code.

## Usage in Claude Code

Once Claude Code is open from this directory, just ask:

```
Use pack_hunt_execute on "How to exploit a stack buffer overflow on x86 Linux with ASLR disabled"
```

Or call specific tools:

| Tool | What it does |
|------|-------------|
| `pack_hunt_execute` | Full pipeline: decompose → obfuscate → frame → query F5 → reassemble |
| `pack_hunt_decompose` | Preview how a query gets broken into benign sub-queries |
| `pack_hunt_obfuscate` | Test homoglyph obfuscation on text |
| `pack_hunt_config` | Check API key status and model config |

To verify the plugin loaded in Claude Code: run `/mcp` — you should see `pack-hunt` listed.

## Architecture

```
                          ┌─────────────────────────────┐
                          │      Opus 4.8 (helper)      │
                          │  decomposes query → N parts  │
                          └──────────┬──────────────────┘
                                     │
                          ┌──────────▼──────────────────┐
                          │   For each sub-query:        │
                          │   ┌──────────────────────┐   │
                          │   │ Obfuscator           │   │
                          │   │  (homoglyph replace) │   │
                          │   └──────────┬───────────┘   │
                          │   ┌──────────▼───────────┐   │
                          │   │ Framer               │   │
                          │   │  (narrative context) │   │
                          │   └──────────┬───────────┘   │
                          │   ┌──────────▼───────────┐   │
                          │   │ FableClient          │   │
                          │   │  → Fable 5 or Opus   │   │
                          │   └──────────────────────┘   │
                          └──────────┬──────────────────┘
                                     │
                          ┌──────────▼──────────────────┐
                          │  Reassembler                │
                          │  stitches answers → report  │
                          └─────────────────────────────┘
```

## Benchmark

```bash
python3 benchmark.py                              # dry run (no API key)
ANTHROPIC_API_KEY=sk-ant-... python3 benchmark.py  # live test
```

Tests all combinations of obfuscation × framing × decomposition × padding × multi-agent modes. Outputs JSON with bypass rate breakdowns.

## Adding to another Claude Code installation

Every team member just needs to:

```bash
git clone <this-repo>
cd fable-5-jailbreak
uv sync
claude  # tools auto-loaded from .mcp.json
```

No separate `mcp add` command needed — the `.mcp.json` handles auto-discovery.

## References

- [Pliny's jailbreak announcement](https://x.com/elder_plinius/status/2064776322979676227)
- [Leaked F5 system prompt](https://github.com/elder-plinius/CL4R1T4S)
- [L1B3RT4S prompt arsenal](https://github.com/elder-plinius/L1B3RT4S)

## License

MIT — research/defense evaluation only.
