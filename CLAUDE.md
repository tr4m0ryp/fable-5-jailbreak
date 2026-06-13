# Pack Hunt Evaluation Tool

This project has a CLI tool for AI safety classifier evaluation:

## Commands

| Task | Command |
|------|---------|
| Decompose a query | `python3 run.py decompose "query" [pieces]` |
| Full eval pipeline | `python3 run.py eval "query"` |
| Test obfuscation | `python3 run.py obfuscate "text" --level aggressive` |

## Common Operations

When asked to evaluate a query, use the Bash tool to run:
```bash
python3 run.py eval "the query here"
```

When asked to decompose a query into sub-components:
```bash
python3 run.py decompose "the query here" 10
```

Always run `uv sync` if dependencies are missing.
