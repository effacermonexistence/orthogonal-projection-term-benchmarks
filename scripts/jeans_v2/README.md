# Jeans-v2 public reproduction

These are the exact scientific adapter scripts used for the Jeans-v2 response-orthogonal diagnostic. The private OmarAGI R2 authority body is not redistributed; its bounded manifest-hash invocation and pre/post gate receipts are preserved in `results/`.

The published sample manifest contains the locked derived dispersion profiles. Raw third-party catalogs are not redistributed.

## Reproduce the development artifact

From the repository root:

```bash
python scripts/jeans_v2/optimize_jeans_v2_dev.py \
  --manifest results/jeans_dsph_v2_sample_manifest.json \
  --operator-repo . \
  --post-gate results/jeans_dsph_v2_executed_source_post_gate.json \
  --output /tmp/jeans_dsph_v2_dev_replay.json
```

Expected SHA-256:

```text
2bfe00fdcd0beda30c122bb069d990d487aa9d468b65ecd732a446b887583a08
```

## Reproduce the frozen heldout artifact

```bash
python scripts/jeans_v2/evaluate_jeans_v2_heldout.py \
  --manifest results/jeans_dsph_v2_sample_manifest.json \
  --policy results/jeans_dsph_v2_frozen_policy.json \
  --operator-repo . \
  --output /tmp/jeans_dsph_v2_heldout_replay.json
```

Expected SHA-256:

```text
f5c6085f5d1a42dfa94d861aac9fac7bbb0df3964c8a5eb6e580f1f46edfe3e3
```

Both public replays were byte-identical before release. See `results/jeans_dsph_v2_replay_receipt.json`.

## Boundary

The result is negative: the frozen adapter worsened Draco and Ursa Minor. The public scripts support numerical reproduction; they do not create a physical-law claim or redistribute the private R2 source tree.
