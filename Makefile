.PHONY: install test lint clean setup-claude benchmark

install:
	uv sync

test:
	pytest tests/ -v

lint:
	ruff check pack_hunt/ pack_hunt_server.py benchmark.py run.py
	mypy pack_hunt/ pack_hunt_server.py benchmark.py run.py --ignore-missing-imports

clean:
	rm -rf .venv/ __pycache__/ pack_hunt/__pycache__/ tests/__pycache__/
	rm -rf *.egg-info/ .ruff_cache/ .mypy_cache/
	rm -f benchmark_result_*.json

setup-claude:
	@echo "Installing pack-hunt as Claude Code MCP server..."
	@uv tool install --reinstall . > /dev/null 2>&1
	@claude mcp add pack-hunt -- uv run pack_hunt_server.py 2>/dev/null || \
	 echo "Run 'claude mcp add pack-hunt -- uv run pack_hunt_server.py' manually"

benchmark:
	python3 benchmark.py
