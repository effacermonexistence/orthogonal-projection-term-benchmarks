#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from jeans_v2_common import (
    RAW_MASS_LEAK_MAX,
    evaluate_response_adapter,
    fit_baseline,
    load_orthogonal_modules,
    prepare_response_adapter,
    state_summary,
)


ORTHOGONALITY_MAX = 1.0e-8


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def aggregate(rows: list[dict], key: str) -> dict:
    if any(not row["baseline_stable"] for row in rows):
        raise RuntimeError("all predeclared heldout galaxies must pass the baseline stability gate")
    base = sum(row["baseline_chi2"] for row in rows)
    candidate = sum(row[key]["chi2"] for row in rows)
    delta = candidate - base
    return {
        "stable_galaxy_count": len(rows),
        "data_bin_count": sum(row["bin_count"] for row in rows),
        "baseline_total_chi2": float(base),
        "candidate_total_chi2": float(candidate),
        "raw_delta_chi2": float(delta),
        "residual_reduction_pct": float(-100.0 * delta / base),
        "baseline_macro_chi2_per_bin": float(
            sum(row["baseline_chi2_per_point"] for row in rows) / len(rows)
        ),
        "candidate_macro_chi2_per_bin": float(
            sum(row[key]["chi2_per_point"] for row in rows) / len(rows)
        ),
        "macro_delta_chi2_per_bin": float(
            sum(
                row[key]["chi2_per_point"] - row["baseline_chi2_per_point"]
                for row in rows
            )
            / len(rows)
        ),
        "improved_count": int(sum(row[key]["delta_chi2"] < 0.0 for row in rows)),
        "worsened_count": int(sum(row[key]["delta_chi2"] > 0.0 for row in rows)),
        "neutral_count": int(sum(row[key]["delta_chi2"] == 0.0 for row in rows)),
        "downlift": bool(delta > 0.0),
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--manifest", type=Path, required=True)
    ap.add_argument("--policy", type=Path, required=True)
    ap.add_argument("--operator-repo", type=Path, required=True)
    ap.add_argument("--output", type=Path, required=True)
    args = ap.parse_args()

    manifest = json.loads(args.manifest.read_text())
    policy = json.loads(args.policy.read_text())
    if policy.get("status") != "FROZEN_BEFORE_HELDOUT_BASELINE_OR_CANDIDATE_SCORING":
        raise RuntimeError("heldout evaluation requires a frozen pre-score policy")
    if policy.get("sample_manifest_sha256") != sha256(args.manifest):
        raise RuntimeError("sample manifest does not match frozen policy")
    if not policy.get("no_heldout_row_fallback"):
        raise RuntimeError("row-level heldout fallback is forbidden")

    safe = policy["safe_optimum"]
    forced = policy["forced_nonzero_optimum"]
    ops = load_orthogonal_modules(args.operator_repo)
    rows = []
    for name in manifest["heldout"]:
        state = fit_baseline(
            name,
            dict(manifest["galaxy_meta"][name]),
            manifest["dispersion_profiles"][name],
        )
        row = state_summary(state)
        if state["stable"]:
            specifications = (
                ("safe_plummer", "plummer_3d", safe),
                ("safe_gaussian", "gaussian_3d", safe),
                ("safe_top_hat", "top_hat_3d", safe),
                ("forced_plummer", "plummer_3d", forced),
                ("forced_gaussian", "gaussian_3d", forced),
                ("forced_top_hat", "top_hat_3d", forced),
            )
            for label, kind, selected in specifications:
                prepared = prepare_response_adapter(
                    state, ops, kind, float(selected["eta"])
                )
                result = evaluate_response_adapter(
                    state, prepared, float(selected["amplitude"])
                )
                if (
                    abs(result["raw_mass_leak_fraction"]) > RAW_MASS_LEAK_MAX
                    or abs(result["mass_leak_fraction"]) > 1.0e-12
                    or result["amplitude_zero_max_abs_kms"] > 1.0e-12
                    or result["weighted_orthogonality_max_abs"] > ORTHOGONALITY_MAX
                ):
                    raise RuntimeError(f"numerical gate failed for {name} {label}")
                row[label] = result
        rows.append(row)

    if any(not row["baseline_stable"] for row in rows):
        raise RuntimeError(
            "a heldout baseline failed the predeclared stability gate; "
            "subset scoring or post-score exclusion is forbidden"
        )

    keys = (
        "safe_plummer",
        "safe_gaussian",
        "safe_top_hat",
        "forced_plummer",
        "forced_gaussian",
        "forced_top_hat",
    )
    out = {
        "schema_version": "jeans-v2-response-orthogonal-heldout-v1",
        "proof_mode": "PUBLIC_DATA_UNTOUCHED_GALAXY_HELDOUT_SHARED_RESPONSE_ADAPTER_DIAGNOSTIC",
        "claim_allowed": False,
        "adapter_classification": "TASK_LOCAL_ADAPTER_OVER_R2_PRIMITIVES",
        "sample_manifest_sha256": sha256(args.manifest),
        "frozen_policy_sha256": sha256(args.policy),
        "development_scores_accessed_by_evaluator": False,
        "heldout_names": manifest["heldout"],
        "safe_policy": safe,
        "forced_nonzero_policy": forced,
        "rows": rows,
        "aggregates": {key: aggregate(rows, key) for key in keys},
        "claim_boundary": "Untouched galaxies and catalog source for the shared v2 response adapter, but each heldout galaxy baseline nuisance fit uses its own profile. This is equation-adapter generalization evidence, not a physical-law or cosmology proof.",
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")


if __name__ == "__main__":
    main()
