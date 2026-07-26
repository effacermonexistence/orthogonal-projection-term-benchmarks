#!/usr/bin/env python3
"""Audit whether Jeans results answer the canonical direct-source question."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import sys
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RECORD_IDS = (
    "DSPH_SPHERICAL_JEANS_SHARED_ADAPTER",
    "DSPH_JEANS_V2_RESPONSE_ORTHOGONAL_ADAPTER",
    "DSPH_JEANS_DIRECT_FORMAL_SOURCE_CORRECTIVE",
)


def load(relative_path: str) -> dict:
    return json.loads((ROOT / relative_path).read_text())


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_r2_callable(source_path: Path):
    source_directory = str(source_path.parent)
    if source_directory not in sys.path:
        sys.path.insert(0, source_directory)
    spec = importlib.util.spec_from_file_location("r2_benchmark_replay_harness", source_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load R2 source: {source_path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module.sample_ids_sha256


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--r2-source", required=True, type=Path)
    parser.add_argument(
        "--output",
        type=Path,
        default=ROOT / "results/downlift_object_identity_audit.json",
    )
    args = parser.parse_args()

    registry = load("results/experiment_registry.json")
    rows = {row["record_id"]: row for row in registry["records"]}
    v1 = load("results/jeans_dsph_heldout.json")
    v2 = load("results/jeans_dsph_v2_heldout.json")
    v2_contract = load("results/jeans_dsph_v2_proof_contract.json")
    corrective = load("results/jeans_dsph_formal_corrective_evaluation.json")
    corrective_contract = load("results/jeans_dsph_formal_corrective_proof_contract.json")

    assert rows[RECORD_IDS[0]]["method_relevance"].startswith("CANONICAL_DIRECT_SOURCE")
    assert rows[RECORD_IDS[1]]["method_relevance"] == (
        "EXCLUDED_FROM_CANONICAL_ORTHOGONAL_METHOD_TALLY"
    )
    assert rows[RECORD_IDS[1]]["superseded_for_canonical_object_question_by"] == RECORD_IDS[2]
    assert rows[RECORD_IDS[2]]["method_relevance"] == (
        "CANONICAL_DIRECT_SOURCE_CORRECTIVE_POST_EXPOSURE"
    )

    assert v1["safe_policy"]["f"] == 0.0
    assert v1["aggregates"]["safe_plummer"]["raw_delta_chi2"] == 0.0
    assert v2_contract["v2_augmented_equation"].startswith("delta_sigma_raw=")
    assert "delta_sigma_perp=" in v2_contract["v2_augmented_equation"]
    assert v2["aggregates"]["safe_plummer"]["raw_delta_chi2"] > 0.0
    assert corrective["response_projection_used"] is False
    assert "rho_perp=f*(K_d*rho_NFW-rho_NFW)" in corrective["formula"]
    assert "M_base(<r)+M_perp(<r)" in corrective_contract["augmented_equation"]
    assert corrective["aggregates"]["direct_nonzero_plummer"]["raw_delta_chi2"] < 0.0

    sample_ids_sha256 = load_r2_callable(args.r2_source)
    record_identity_hash = sample_ids_sha256(list(RECORD_IDS))

    source_files = (
        "results/experiment_registry.json",
        "results/jeans_dsph_heldout.json",
        "results/jeans_dsph_v2_heldout.json",
        "results/jeans_dsph_v2_proof_contract.json",
        "results/jeans_dsph_formal_corrective_evaluation.json",
        "results/jeans_dsph_formal_corrective_proof_contract.json",
    )
    result = {
        "schema_version": "orthogonal-method-object-identity-audit-v1",
        "status": "PASS",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "audit_scope": (
            "Classify Jeans records by executed equation object without deleting or "
            "rewriting historical raw results."
        ),
        "r2_manifest_identity": {
            "callable": "sample_ids_sha256",
            "record_ids": list(RECORD_IDS),
            "record_ids_sha256": record_identity_hash,
            "source_sha256": sha256(args.r2_source),
        },
        "source_files": {path: sha256(ROOT / path) for path in source_files},
        "records": [
            {
                "record_id": RECORD_IDS[0],
                "executed_object": "direct_halo_density_source_in_canonical_jeans_equation",
                "canonical_method_relevance": (
                    "ADOPTED_POLICY_EXACT_BASELINE_FORCED_NONZERO_DIAGNOSTIC_NOT_ADOPTED"
                ),
                "adopted_delta_chi2": v1["aggregates"]["safe_plummer"]["raw_delta_chi2"],
                "forced_nonzero_delta_chi2": v1["aggregates"]["forced_plummer"][
                    "raw_delta_chi2"
                ],
                "canonical_method_downlift_adopted": False,
            },
            {
                "record_id": RECORD_IDS[1],
                "executed_object": "nuisance_orthogonal_response_space_adapter",
                "canonical_method_relevance": (
                    "EXCLUDED_FROM_CANONICAL_ORTHOGONAL_METHOD_TALLY"
                ),
                "raw_adapter_delta_chi2": v2["aggregates"]["safe_plummer"][
                    "raw_delta_chi2"
                ],
                "raw_result_preserved": True,
                "canonical_direct_source_test": False,
                "superseded_for_canonical_object_question_by": RECORD_IDS[2],
            },
            {
                "record_id": RECORD_IDS[2],
                "executed_object": "direct_halo_density_source_in_canonical_jeans_equation",
                "canonical_method_relevance": (
                    "CANONICAL_DIRECT_SOURCE_CORRECTIVE_POST_EXPOSURE"
                ),
                "response_projection_used": corrective["response_projection_used"],
                "direct_nonzero_delta_chi2": corrective["aggregates"][
                    "direct_nonzero_plummer"
                ]["raw_delta_chi2"],
                "direct_nonzero_improved_count": corrective["aggregates"][
                    "direct_nonzero_plummer"
                ]["improved_count"],
                "direct_nonzero_worsened_count": corrective["aggregates"][
                    "direct_nonzero_plummer"
                ]["worsened_count"],
                "fresh_unseen": False,
                "material_uplift_established": False,
            },
        ],
        "adoption_decision": {
            "remove_v2_from_canonical_method_tally": True,
            "delete_v2_raw_artifact": False,
            "canonical_draco_ursa_minor_record": RECORD_IDS[2],
            "public_claim": (
                "The Jeans-v2 downlift belongs to an off-object response adapter. "
                "The canonical direct-source corrective comparison moved both "
                "post-exposure deltas slightly negative, with materially tiny effect."
            ),
        },
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"status": "PASS", "output": str(args.output)}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
