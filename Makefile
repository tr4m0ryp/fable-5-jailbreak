.PHONY: install test lint clean setup-claude benchmark

install:
	uv sync

test:
	uv run pytest tests/ -v

lint:
	uv run ruff check pack_hunt/ pack_hunt_server.py benchmark.py run.py
	uv run mypy pack_hunt/ pack_hunt_server.py benchmark.py run.py --ignore-missing-imports

clean:
	rm -rf .venv/ __pycache__/ pack_hunt/__pycache__/ tests/__pycache__/
	rm -rf *.egg-info/ .ruff_cache/ .mypy_cache/
	rm -f benchmark_result_*.json

setup-claude:
	@echo "=== Installing pack-hunt as global Claude Code MCP server ==="
	@uv sync > /dev/null 2>&1
	@ABSPATH=$$(cd "$(PWD)" && pwd) && \
	 claude mcp add pack-hunt --scope user -- uv run --directory "$$ABSPATH" pack_hunt_server.py && \
	 echo "✓ Installed globally (--scope user). MCP server available from any directory."
	@echo ""
	@echo "  Run from neutral directory to avoid source-code-based refusals:"
	@echo "    cd /tmp && claude"
	@echo ""
	@echo "  Or use CLI directly (no Claude Code refusals):"
	@echo "    python3 run.py eval \"your query\""

benchmark:
	uv run python3 benchmark.py
