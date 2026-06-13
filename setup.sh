#!/usr/bin/env bash
set -euo pipefail

echo "=== Pack Hunt MCP Plugin Setup ==="

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "ERROR: python3 not found. Install Python 3.11+ first."
    exit 1
fi
echo "✓ Python $(python3 --version)"

# Check pip
if ! command -v pip3 &> /dev/null; then
    echo "ERROR: pip3 not found."
    exit 1
fi

# Create virtual environment
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv .venv
fi
echo "✓ Virtual environment"

# Activate and install deps
source .venv/bin/activate
echo "Installing dependencies..."
pip install -q -r requirements.txt
echo "✓ Dependencies installed"

# Install the package in dev mode
pip install -q -e .
echo "✓ Package installed"

# Check for .env
if [ ! -f ".env" ]; then
    if [ -f ".env.example" ]; then
        cp .env.example .env
        echo "✓ Created .env from .env.example"
        echo "  → Edit .env and add your ANTHROPIC_API_KEY"
    fi
else
    echo "✓ .env exists"
fi

# Register with Claude Code
echo ""
echo "=== Register MCP Server with Claude Code ==="
echo ""
echo "Run this to add the pack-hunt tool to Claude Code:"
echo ""
echo "  claude mcp add --transport stdio pack-hunt -- \\"
echo "    uv run --directory $(pwd) pack_hunt_server.py"
echo ""
echo "Or from within Claude Code, use:"
echo "  /mcp add"
echo ""
echo "=== Done ==="
echo "Quick test: python pack_hunt_server.py --help  # verify imports"
echo "Benchmark:  python benchmark.py               # dry run (no API key)"
echo "Full test:  ANTHROPIC_API_KEY=sk-... python benchmark.py"
