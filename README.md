# Orthogonal Projection Term — Cosmology Residual Benchmarks

**OmarAGI research record.** This repository preserves the equations, frozen insertions, public-data provenance, diagnostic scores, matched controls, and negative results from an exploratory orthogonal redistribution-term program.

The object tested throughout the core lanes is:

$$
\mathcal O_\perp[X] = f_\perp\left(\mathcal K_d[X]-X\right),
\qquad
X_{\mathrm{aug}}=(1-f_\perp)X+f_\perp\mathcal K_d[X].
$$

It does **not** create mass by construction when the kernel is normalized on the full domain; it redistributes a selected component. The earlier fixed-scale lanes freeze `f_perp = 0.30` and `d = 16 kpc`. The SPARC lane freezes one development-selected equation adapter, `f = 1.0` and `d_g = 0.125 R_disk,g`, before heldout evaluation. The first dwarf-spheroidal Jeans lane independently calibrates the same density-adapter grammar and selects the safe baseline, `f = 0`. A separate Jeans-v2 experiment calibrates a nuisance-orthogonal equation-response adapter on four development galaxies and freezes it before evaluating Draco and Ursa Minor from a different public catalog.

## What the record shows

| Diagnostic | Frozen directional result | Matched-control result | Evidence boundary |
|---|---:|---|---|
| HFF public lens-model maps, 6 clusters | Negative residual delta in 6/6; Plummer-like reductions 4.96%–27.99% | Generic Gaussian/top-hat also improved 6/6 and beat Plummer-like in 5/6 | Generic low-pass/model-product effect |
| AS1063 true-density B2 | 19.857% residual reduction | Gaussian 19.011%; top-hat 18.681% | Plummer slightly best, but specificity unresolved |
| SIDM Concerto Halo000 | 29.366% residual reduction | Gaussian/top-hat about 29.44% | Direction pass; Plummer specificity fail |
| SIDM Concerto Halo352, fresh target | 41.000% residual reduction | Gaussian 42.129%; top-hat 42.581% | Direction pass; Plummer specificity fail |
| SPARC rotation curves, shared-adapter heldout | 208.845 → 199.589 χ²; 4.432% reduction; 5/6 stable galaxies improved | Gaussian 2.620%; top-hat 2.413%; Plummer best in aggregate | Shared `f/eta` held out; per-galaxy NFW nuisances fitted; diagnostic, not clean predictive proof |
| Dwarf-spheroidal spherical Jeans, shared-adapter heldout | Safe calibration selected `f=0`; forced Plummer 35.352827 → 35.354732 χ² | Gaussian/top-hat were also near-neutral but adverse in aggregate | Valid negative result; no adapter uplift |
| Jeans-v2 nuisance-orthogonal response, untouched-galaxy heldout | 22.835649 → 24.085741 χ²; -5.474% residual reduction; 0/2 improved | Gaussian -5.331%; top-hat -3.202%; all three worsened both galaxies | Clean negative generalization result on Draco and Ursa Minor; no v2 uplift |
| N13-style development likelihood | raw delta chi-square -1.2543 | 20th percentile under null; baryonic countermodel absorbs residual | Development negative / not proof |
| H(z) background-fluid lane | raw delta chi-square -0.00874 | AIC and BIC worsen | Separate Program C term; no real uplift |

**Supported reading:** inserting a frozen redistribution term can move selected public model products, parametric profiles, or heldout shared-adapter rotation-curve residuals in the favorable direction under the stored metric. It does not do so universally: Jeans-v1 selected the unmodified baseline, and Jeans-v2 worsened both untouched heldout galaxies after its development-selected response rule was frozen.

**Not supported:** a new physical source, a Plummer-specific mechanism, a detection of hidden geometry, a replacement for GR/LambdaCDM, or an observational-likelihood improvement. In the strongest fresh 3D control, generic smoothers performed slightly better than Plummer.

## Why publish this

Scientific iteration is easier to audit when positive deltas, failed specificity tests, reused samples, and superseded interpretations remain in one durable public record. This repository therefore includes the negative results rather than hiding them.

## Repository map

- [`docs/OPERATOR.md`](docs/OPERATOR.md) — exact 2D/3D operator definitions and kernel lineage.
- [`docs/EQUATION_INSERTIONS.md`](docs/EQUATION_INSERTIONS.md) — Poisson, lensing, halo-profile, Jeans, Friedmann, and Einstein-container placements.
- [`docs/EXPERIMENT_REGISTRY.md`](docs/EXPERIMENT_REGISTRY.md) — what was run and what is or is not independent.
- [`docs/SPARC_ROTATION_CURVE_ADAPTER.md`](docs/SPARC_ROTATION_CURVE_ADAPTER.md) — the full SPARC equation, sample lock, dev/heldout split, controls, row results, and audit boundary.
- [`docs/JEANS_DSPH_ADAPTER.md`](docs/JEANS_DSPH_ADAPTER.md) — the dwarf-spheroidal Jeans equation placement, calibration, heldout negative result, controls, and verification.
- [`docs/JEANS_DSPH_RESPONSE_ADAPTER_V2.md`](docs/JEANS_DSPH_RESPONSE_ADAPTER_V2.md) — the nuisance-orthogonal response construction, different-catalog heldout split, frozen downlift, and independent audit.
- [`docs/DATA_PROVENANCE.md`](docs/DATA_PROVENANCE.md) — external sources and checksums.
- [`docs/CLAIM_BOUNDARIES.md`](docs/CLAIM_BOUNDARIES.md) — exact public claim limits.
- [`results/`](results/) — sanitized machine-readable scores with upstream artifact hashes.
- [`src/orthogonal_projection_term/`](src/orthogonal_projection_term/) — reusable operator, kernel, radial convolution, and scoring code.
- [`scripts/`](scripts/) — public-data reproduction adapters and integrity verifier.
- [`audits/RED_TEAM_FINDINGS.md`](audits/RED_TEAM_FINDINGS.md) — strongest adversarial findings.

## Verify the published record

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e '.[test]'
python scripts/verify_published_results.py
pytest -q
```

To reproduce one HFF cluster after obtaining the public FITS maps, take
that cluster's frozen `d_arcsec` from
[`results/hff_six_cluster_transfer.json`](results/hff_six_cluster_transfer.json):

```bash
python scripts/reproduce_hff_transfer.py \
  --target CATS_kappa_best.fits \
  --reference GLAFIC_kappa_best.fits \
  --reference WILLIAMS_kappa_best.fits \
  --d-arcsec <stored-d-arcsec> \
  --output reproduced_cluster.json
```

The adapter WCS-resamples the reference maps, applies the frozen 60-arcsec
scoring mask, and half-mass-matches both generic controls to the discrete
finite Plummer-like kernel before scoring.

Large external FITS archives and simulation tables are not redistributed. Download instructions and source hashes are in [`docs/DATA_PROVENANCE.md`](docs/DATA_PROVENANCE.md).

The SPARC public-data reproduction path is documented in
[`scripts/sparc/README.md`](scripts/sparc/README.md). Its full development grid,
heldout rows, matched controls, verification receipt, and pre-heldout failures
are preserved under [`results/`](results/).

The dwarf-spheroidal Jeans path is documented in
[`scripts/jeans/README.md`](scripts/jeans/README.md). Its full development grid,
safe and forced policies, heldout rows, matched controls, verification receipt,
and pre-heldout failures are also preserved under [`results/`](results/).

The separate Jeans-v2 path is documented in
[`scripts/jeans_v2/README.md`](scripts/jeans_v2/README.md). Its public dev and
heldout replays are byte-identical to the published artifacts; the result is a
preserved negative generalization result, not a repaired or hidden failure.

## License and citation

Code is released under the MIT License. Cite the repository using [`CITATION.cff`](CITATION.cff). Source datasets retain their original licenses and attribution requirements.
