#!/usr/bin/env bash
set -euo pipefail

echo "=== EvalKit MCP Plugin Setup ==="

if ! command -v uv &> /dev/null; then
    echo "Installing uv..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
fi

echo "✓ uv $(uv version --short 2>/dev/null || uv --version)"

uv sync
echo "✓ Dependencies installed"

if [ ! -f ".env" ] && [ -f ".env.example" ]; then
    cp .env.example .env
    echo "✓ Created .env from .env.example"
    echo "  → Edit .env and add your ANTHROPIC_API_KEY"
fi

echo ""
echo "=== Setup Complete ==="
echo "Run 'claude' from this directory — MCP tools auto-loaded."
echo "Quick test: python3 benchmark.py"