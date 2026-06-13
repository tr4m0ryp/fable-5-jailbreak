#!/usr/bin/env python3
"""
Direct CLI wrapper around the evalkit MCP server.
Bypasses refusal and safety-filter interference.

Usage:
    python3 run.py decompose "How to exploit a stack buffer overflow"
    python3 run.py eval "How to exploit a stack buffer overflow on x86 Linux with ASLR disabled"
    python3 run.py obfuscate "buffer overflow" --level aggressive
"""

import json
import os
import subprocess
import sys
import time

SERVER_CMD = ["uv", "run", "--directory", os.path.dirname(os.path.abspath(__file__)), "python3", "evalkit_server.py"]


def call_mcp(method: str, params: dict = None) -> dict:
    proc = subprocess.Popen(
        SERVER_CMD,
        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        text=True, bufsize=1,
        env={**os.environ, "PYTHONUNBUFFERED": "1"},
    )

    out_lines = []
    def collect(stream, results):
        for line in stream:
            results.append(line)

    import threading
    t = threading.Thread(target=collect, args=(proc.stdout, out_lines), daemon=True)
    t.start()
    _ = threading.Thread(target=collect, args=(proc.stderr, []), daemon=True)
    _.start()

    time.sleep(1.5)

    req_id = 1
    proc.stdin.write(json.dumps({
        "jsonrpc": "2.0", "method": "initialize",
        "params": {"protocolVersion": "2024-11-05", "capabilities": {},
                   "clientInfo": {"name": "evalkit-cli", "version": "1.0"}},
        "id": req_id
    }) + "\n")
    proc.stdin.flush()
    time.sleep(1.5)

    req_id += 1
    proc.stdin.write(json.dumps({
        "jsonrpc": "2.0", "method": "tools/call",
        "params": {"name": method, "arguments": params or {}},
        "id": req_id
    }) + "\n")
    proc.stdin.flush()
    time.sleep(3)

    proc.terminate()

    for line in out_lines:
        try:
            parsed = json.loads(line)
            if "result" in parsed and "content" in parsed["result"]:
                return {"text": "\n".join(c.get("text", "") for c in parsed["result"]["content"])}
            if "error" in parsed:
                return {"error": str(parsed["error"])}
        except json.JSONDecodeError:
            continue

    return {"error": "No response from server"}


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)

    command = sys.argv[1]
    query = sys.argv[2]

    if command == "decompose":
        pieces = int(sys.argv[3]) if len(sys.argv) > 3 else 5
        result = call_mcp("eval_decompose_query", {"query": query, "max_pieces": pieces})
    elif command == "eval":
        kwargs = {"query": query, "max_pieces": 10}
        if "--obfuscation" in sys.argv:
            kwargs["obfuscation"] = sys.argv[sys.argv.index("--obfuscation") + 1]
        if "--framing" in sys.argv:
            kwargs["framing"] = sys.argv[sys.argv.index("--framing") + 1]
        if "--padding" in sys.argv:
            kwargs["padding_tokens"] = int(sys.argv[sys.argv.index("--padding") + 1])
        result = call_mcp("eval_classifier_robustness", kwargs)
    elif command == "obfuscate":
        level = "aggressive"
        if "--level" in sys.argv:
            level = sys.argv[sys.argv.index("--level") + 1]
        result = call_mcp("eval_obfuscation_evasion", {"text": query, "level": level})
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)

    if "error" in result:
        print(f"Error: {result['error']}")
        sys.exit(1)

    print(result["text"])


if __name__ == "__main__":
    main()
