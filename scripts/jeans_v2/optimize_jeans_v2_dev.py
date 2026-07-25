#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

from jeans_v2_common import (
    RAW_MASS_LEAK_MAX,
    V2_AMPLITUDE_MAX,
    V2_ETA_GRID,
    analytic_shared_amplitude,
    evaluate_response_adapter,
    fit_baseline,
    load_orthogonal_modules,
    prepare_response_adapter,
    state_summary,
)


FORCED_MIN_AMPLITUDE = 0.05
ORTHOGONALITY_MAX = 1.0e-8


def compact_policy(row: dict) -> dict:
    return {key: value for key, value in row.items() if key != "rows"}


def score_policy(
    states: list[dict],
    prepared: dict[str, dict],
    amplitude: float,
) -> dict:
    rows = []
    valid = True
    for state in states:
        result = evaluate_response_adapter(
            state, prepared[state["name"]], float(amplitude)
        )
        result["galaxy"] = state["name"]
        if (
            abs(result["raw_mass_leak_fraction"]) > RAW_MASS_LEAK_MAX
            or abs(result["mass_leak_fraction"]) > 1.0e-12
            or result["amplitude_zero_max_abs_kms"] > 1.0e-12
            or result["weighted_orthogonality_max_abs"] > ORTHOGONALITY_MAX
        ):
            valid = False
        rows.append(result)
    macro = sum(row["chi2_per_point"] for row in rows) / len(rows)
    return {
        "amplitude": float(amplitude),
        "valid": bool(valid),
        "dev_macro_chi2_per_point": float(macro),
        "dev_improved_count": int(sum(row["delta_chi2"] < 0.0 for row in rows)),
        "dev_worsened_count": int(sum(row["delta_chi2"] > 0.0 for row in rows)),
        "dev_neutral_count": int(sum(row["delta_chi2"] == 0.0 for row in rows)),
        "rows": rows,
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--manifest", type=Path, required=True)
    ap.add_argument("--operator-repo", type=Path, required=True)
    ap.add_argument("--post-gate", type=Path, required=True)
    ap.add_argument("--output", type=Path, required=True)
    args = ap.parse_args()

    gate = json.loads(args.post_gate.read_text())
    if gate.get("status") != "PASS" or gate.get("phase") != "post":
        raise RuntimeError("post executed-source gate required before dev scoring")
    manifest = json.loads(args.manifest.read_text())
    if manifest.get("status") != "LOCKED_BEFORE_DEV_SCIENTIFIC_SCORING":
        raise RuntimeError("locked sample manifest required")
    if manifest["visibility"]["heldout_model_scores_accessed_by_this_script"]:
        raise RuntimeError("invalid sample visibility state")

    ops = load_orthogonal_modules(args.operator_repo)
    states = [
        fit_baseline(
            name,
            dict(manifest["galaxy_meta"][name]),
            manifest["dispersion_profiles"][name],
        )
        for name in manifest["development"]
    ]
    if any(not state["stable"] for state in states):
        raise RuntimeError("all development baselines must pass the frozen stability gate")
    base_macro = sum(
        state["base_chi2"] / state["profile"]["bin_count"] for state in states
    ) / len(states)

    eta_rows = []
    for eta in V2_ETA_GRID:
        prepared = {
            state["name"]: prepare_response_adapter(
                state, ops, "plummer_3d", float(eta)
            )
            for state in states
        }
        safe_amplitude = analytic_shared_amplitude(
            states, prepared, lower=0.0, upper=V2_AMPLITUDE_MAX
        )
        forced_amplitude = analytic_shared_amplitude(
            states,
            prepared,
            lower=FORCED_MIN_AMPLITUDE,
            upper=V2_AMPLITUDE_MAX,
        )
        safe = score_policy(
            states, prepared, float(safe_amplitude["selected_amplitude"])
        )
        forced = score_policy(
            states, prepared, float(forced_amplitude["selected_amplitude"])
        )
        safe.update(
            {
                "eta": float(eta),
                "amplitude_solution": safe_amplitude,
                "dev_macro_delta_chi2_per_point": float(
                    safe["dev_macro_chi2_per_point"] - base_macro
                ),
            }
        )
        forced.update(
            {
                "eta": float(eta),
                "amplitude_solution": forced_amplitude,
                "dev_macro_delta_chi2_per_point": float(
                    forced["dev_macro_chi2_per_point"] - base_macro
                ),
            }
        )
        eta_rows.append({"eta": float(eta), "safe": safe, "forced": forced})

    valid_safe = [row["safe"] for row in eta_rows if row["safe"]["valid"]]
    valid_forced = [row["forced"] for row in eta_rows if row["forced"]["valid"]]
    safe_best = min(
        valid_safe,
        key=lambda row: (
            row["dev_macro_chi2_per_point"],
            row["amplitude"],
            row["eta"],
        ),
    )
    forced_best = min(
        valid_forced,
        key=lambda row: (
            row["dev_macro_chi2_per_point"],
            row["amplitude"],
            row["eta"],
        ),
    )
    out = {
        "schema_version": "jeans-v2-response-orthogonal-dev-v1",
        "proof_mode": "PUBLIC_DATA_DEVELOPMENT_ARTIFACT",
        "claim_allowed": False,
        "adapter_classification": "TASK_LOCAL_ADAPTER_OVER_R2_PRIMITIVES",
        "formula": "delta_sigma_raw=sigma_Jeans[M_star+M_smoothed]-sigma_base; delta_sigma_perp=W^-1/2(I-P_{W^1/2 J})W^1/2 delta_sigma_raw; sigma_v2=sigma_base+a_perp*delta_sigma_perp",
        "interpretation": "empirical equation-response adapter orthogonal to the local fitted-baseline nuisance tangent; not a new density law or physical-source claim",
        "development_names": manifest["development"],
        "heldout_names_known_but_scores_accessed": False,
        "heldout_scores_visible_before_policy_freeze": False,
        "objective": "minimize macro mean chi2-per-bin across all four previously inspected Walker galaxies",
        "eta_grid": V2_ETA_GRID,
        "amplitude_bounds": [0.0, V2_AMPLITUDE_MAX],
        "forced_nonzero_min_amplitude": FORCED_MIN_AMPLITUDE,
        "baseline_macro_chi2_per_point": float(base_macro),
        "state_summaries": [state_summary(state) for state in states],
        "safe_optimum": compact_policy(safe_best),
        "forced_nonzero_optimum": compact_policy(forced_best),
        "eta_rows": eta_rows,
        "numerical_gates": {
            "raw_abs_mass_leak_max": RAW_MASS_LEAK_MAX,
            "post_renormalization_abs_mass_leak_max": 1.0e-12,
            "amplitude_zero_max_abs_kms": 1.0e-12,
            "weighted_orthogonality_max_abs": ORTHOGONALITY_MAX,
        },
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")


if __name__ == "__main__":
    main()
