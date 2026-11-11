"""Replay fixed upstream timings without networking or sleeping."""

import math


def validate_config(config):
    if not isinstance(config, dict):
        raise ValueError("config must be an object")
    if config.get("service") != "document-flow":
        raise ValueError("service must be document-flow")
    dependency = config.get("dependency")
    if not isinstance(dependency, dict):
        raise ValueError("dependency must be an object")
    limits = {
        "timeout_ms": (1, 2000),
        "max_attempts": (1, 5),
        "retry_backoff_ms": (0, 1000),
    }
    for name, (minimum, maximum) in limits.items():
        value = dependency.get(name)
        if type(value) is not int or not minimum <= value <= maximum:
            raise ValueError(f"{name} must be an integer in [{minimum}, {maximum}]")
    return dependency


def percentile(values, fraction):
    """Use the nearest-rank definition."""
    return sorted(values)[math.ceil(len(values) * fraction) - 1]


def replay(config, requests):
    dependency = validate_config(config)
    if not requests:
        raise ValueError("replay dataset must not be empty")
    timeout = dependency["timeout_ms"]
    rows = []
    for request in requests:
        elapsed = 0
        attempts = []
        for number in range(1, dependency["max_attempts"] + 1):
            duration = request["upstream_latency_ms"]
            completed = duration <= timeout
            elapsed += min(duration, timeout)
            attempts.append({
                "attempt": number,
                "duration_ms": min(duration, timeout),
                "outcome": "ok" if completed else "timeout",
            })
            if completed:
                break
            if number < dependency["max_attempts"]:
                elapsed += dependency["retry_backoff_ms"]
        rows.append({
            "request_id": request["request_id"],
            "status": 200 if completed else 504,
            "elapsed_ms": elapsed,
            "attempts": attempts,
        })
    successful = sum(row["status"] == 200 for row in rows)
    attempt_count = sum(len(row["attempts"]) for row in rows)
    return {
        "summary": {
            "request_count": len(rows),
            "success_rate": successful / len(rows),
            "p95_elapsed_ms": percentile([row["elapsed_ms"] for row in rows], 0.95),
            "max_elapsed_ms": max(row["elapsed_ms"] for row in rows),
            "upstream_attempts": attempt_count,
            "attempts_per_request": attempt_count / len(rows),
        },
        "requests": rows,
    }


def verify(summary):
    """Fixed exercise targets, independent of the submitted configuration."""
    checks = [
        ("success_rate", summary["success_rate"] >= 0.99, ">= 0.99"),
        ("p95_elapsed_ms", summary["p95_elapsed_ms"] <= 1200, "<= 1200"),
        ("max_elapsed_ms", summary["max_elapsed_ms"] <= 2500, "<= 2500"),
        ("attempts_per_request", summary["attempts_per_request"] <= 1.10, "<= 1.10"),
    ]
    return {
        "passed": all(passed for _, passed, _ in checks),
        "checks": [
            {"metric": name, "actual": summary[name], "target": target, "passed": passed}
            for name, passed, target in checks
        ],
    }
