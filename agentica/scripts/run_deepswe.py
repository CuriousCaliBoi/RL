#!/usr/bin/env python3
"""Minimal script to query a DeepSWE model served by vLLM.

This script expects a vLLM server exposing an OpenAI-compatible API
at the given ``--api-url`` (defaults to ``http://localhost:30000/v1``).
Use ``--dry-run`` to print the request payload without sending it.
"""

from __future__ import annotations

import argparse
import json
from typing import Any, Dict

try:  # Lazy import so --dry-run works without optional deps
    import requests
except ModuleNotFoundError:  # pragma: no cover - dependency may not be installed
    requests = None


def build_payload(model: str, prompt: str) -> Dict[str, Any]:
    """Construct the chat completion payload for the given prompt."""
    return {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Run DeepSWE via local vLLM")
    parser.add_argument("--prompt", default="Hello from DeepSWE!", help="User prompt")
    parser.add_argument(
        "--api-url",
        default="http://localhost:30000/v1",
        help="Base URL of the vLLM OpenAI-compatible API",
    )
    parser.add_argument(
        "--model",
        default="agentica-org/DeepSWE-Preview",
        help="Model name served by vLLM",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the payload without making a request",
    )
    args = parser.parse_args()

    payload = build_payload(args.model, args.prompt)

    if args.dry_run:
        print(json.dumps(payload, indent=2))
        return 0

    if requests is None:
        print("The 'requests' library is required to contact the API. Install it or use --dry-run.")
        return 1

    try:
        response = requests.post(
            f"{args.api_url}/chat/completions", json=payload, timeout=120
        )
        response.raise_for_status()
    except Exception as exc:  # pragma: no cover - best effort error reporting
        print(f"Request failed: {exc}")
        return 1

    data = response.json()
    message = data.get("choices", [{}])[0].get("message", {}).get("content", "")
    print(message)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
