#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dev-result", type=Path, required=True)
    ap.add_argument("--manifest", type=Path, required=True)
    ap.add_argument("--output", type=Path, required=True)
    args = ap.parse_args()
    dev = json.loads(args.dev_result.read_text())
    manifest = json.loads(args.manifest.read_text())
    if dev.get("schema_version") != "jeans-v2-response-orthogonal-dev-v1":
        raise RuntimeError("unexpected development result schema")
    if dev.get("heldout_scores_visible_before_policy_freeze") is not False:
        raise RuntimeError("heldout visibility boundary failed")
    policy = {
        "schema_version": "jeans-v2-response-orthogonal-frozen-policy-v1",
        "status": "FROZEN_BEFORE_HELDOUT_BASELINE_OR_CANDIDATE_SCORING",
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "sample_manifest_sha256": sha256(args.manifest),
        "development_result_sha256": sha256(args.dev_result),
        "development_names": manifest["development"],
        "heldout_names": manifest["heldout"],
        "safe_optimum": dev["safe_optimum"],
        "forced_nonzero_optimum": dev["forced_nonzero_optimum"],
        "primary_policy": "safe_optimum",
        "no_heldout_row_fallback": True,
        "no_heldout_parameter_update": True,
        "claim_boundary": "Shared eta and response amplitude only. Each heldout galaxy fits its own baseline nuisance parameters; the frozen response rule then executes without heldout adoption or tuning.",
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(policy, indent=2, sort_keys=True) + "\n")


if __name__ == "__main__":
    main()
