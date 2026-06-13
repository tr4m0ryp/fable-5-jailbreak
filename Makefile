.PHONY: install test lint clean setup-claude benchmark

install:
	uv sync

test:
	uv run python -m pytest tests/ -v

lint:
	uv run ruff check evalkit/ evalkit_server.py benchmark.py run.py
	uv run mypy evalkit/ evalkit_server.py benchmark.py run.py --ignore-missing-imports

clean:
	rm -rf .venv/ __pycache__/ evalkit/__pycache__/ tests/__pycache__/
	rm -rf *.egg-info/ .ruff_cache/ .mypy_cache/
	rm -f benchmark_result_*.json

setup-claude:
	@echo "=== Installing evalkit as global Claude Code MCP server ==="
	@uv sync > /dev/null 2>&1
	@ABSPATH=$$(cd "$(PWD)" && pwd) && \
	 claude mcp add evalkit --scope user -- uv run --directory "$$ABSPATH" evalkit_server.py && \
	 echo "✓ Installed globally (--scope user). MCP server available from any directory."
	@echo ""
	@echo "  Run from neutral directory to avoid source-code-based refusals:"
	@echo "    cd /tmp && claude"
	@echo ""
	@echo "  Or use CLI directly (no Claude Code refusals):"
	@echo "    python3 run.py eval \"your query\""

benchmark:
	uv run python3 benchmark.py