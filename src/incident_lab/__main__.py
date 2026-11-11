"""Command-line entry point for the offline lab."""

import argparse
import hashlib
import json
from pathlib import Path
import sys

from incident_lab.model import replay, verify


def main():
    parser = argparse.ArgumentParser(description="Replay a synthetic incident offline.")
    parser.add_argument("command", choices=["replay", "verify"])
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--dataset", type=Path, default=Path("kilder/replay.json"))
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    try:
        config_bytes = args.config.read_bytes()
        dataset_bytes = args.dataset.read_bytes()
        config = json.loads(config_bytes)
        dataset = json.loads(dataset_bytes)
        result = replay(config, dataset["requests"])
        result["inputs"] = {
            "config": str(args.config),
            "config_sha256": hashlib.sha256(config_bytes).hexdigest(),
            "dataset": str(args.dataset),
            "dataset_sha256": hashlib.sha256(dataset_bytes).hexdigest(),
        }
        if args.command == "verify":
            result["verification"] = verify(result["summary"])
        output = json.dumps(result, indent=2) + "\n"
        if args.output:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(output, encoding="utf-8")
        print(output, end="")
        return 1 if args.command == "verify" and not result["verification"]["passed"] else 0
    except (OSError, ValueError, KeyError, TypeError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
