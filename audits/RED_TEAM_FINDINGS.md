# Adversarial audit findings

This file records the strongest challenges that survived arithmetic and executed-path review.

## 1. Development sample reuse

Much of the early program reused one five-cluster N13-style likelihood under different model or channel labels. Those views are useful for debugging but are not independent confirmations.

## 2. Post-selection gate contamination

The early “beyond-null” interpretation depended on gates refined after observing development behavior. The ungated M1 result was at the 20th percentile of the stored null distribution. This repository therefore labels the chain as development-only.

## 3. Baryonic countermodel absorption

The academic baryonic/cored-halo countermodel reduced the development residual far more than the M1 term. The small M3-over-M2 change did not exceed the expected scale of additional flexibility.

## 4. HFF generic-smoothing explanation

Plummer-like, Gaussian, and top-hat kernels all reduced the CATS-to-reference-team discrepancy in all six clusters. Generic controls beat Plummer-like in five of six. The map result is therefore attributed to generic low-pass redistribution under the current score.

## 5. Fresh 3D specificity failure

On the score-blind Halo352 target:

- Plummer: 41.000% reduction
- Gaussian: 42.129% reduction
- top-hat: 42.581% reduction

The run is deterministic, uses the correct 3D Plummer density kernel, has exact `f=0` recovery, and has no optimizer, fallback, or adoption gate. It cleanly rejects Plummer specificity for this setup.

## 6. Mechanically favorable cusp-to-core direction

The SIDM references are cored and the CDM baselines are cusped. Low-pass redistribution removes cusp power, so a negative directional delta is expected for many smoothers. The direction alone carries little operator-specific information.

## 7. SPARC shared-adapter boundary

The SPARC result adds a different public observational domain and a real
dev/heldout split for shared adapter parameters. It does not create a clean
predictive lane because each heldout curve still fits its own NFW baseline
nuisance parameters. Plummer was best in aggregate, but all three matched
kernels improved 5/6 stable galaxies, one heldout baseline was unstable, and
the stable sample is too small for confirmatory or kernel-specific claims.

## 8. Dwarf-spheroidal Jeans rejection

The Jeans lane calibrated the shared adapter on Sextans and Fornax before
opening Sculptor and Carina. The safe development policy selected `f=0`.
The separately frozen forced-nonzero Plummer policy slightly worsened both
heldout galaxies (`delta chi-square = +0.001905307`), while matched generic
controls were also near-neutral and adverse in aggregate. The correct result
is no adapter uplift, not a small positive effect.

## 9. Jeans-v2 untouched-galaxy downlift

Jeans-v2 changed the construction rather than retuning Jeans-v1: the raw
halo-smoothing response was projected orthogonally to the local weighted
baseline-nuisance tangent, and one shared scale/amplitude pair was selected on
Carina, Fornax, Sculptor, and Sextans. The policy was frozen before scoring
Draco or Ursa Minor from a different catalog.

The frozen Plummer response worsened both heldout galaxies
(`delta chi-square = +1.250092317`; residual reduction `-5.4743%`).
Matched Gaussian and top-hat responses also worsened both. The development
amplitude hit its declared upper bound, but widening that bound after heldout
inspection would invalidate the locked experiment. The valid result is
`UNTOUCHED_GALAXY_HELDOUT_DOWNLIFT_NO_GENERALIZATION`.

## 10. Jeans executed-object correction

Jeans-v2 answered a response-adapter question rather than the requested direct canonical-source insertion. The record now labels that mismatch explicitly and preserves both experiments. In the corrected formal-source run, development again selected the baseline `f=0`. A frozen nonzero diagnostic moved both post-exposure evaluation deltas negative, but only by `delta chi-square = -0.001159399` (`0.005077%`). That establishes executed-object correction and a tiny directional delta, not material uplift, fresh proof, or adoption support.

## 11. X-COP direct equation: direction survives, specificity remains open

The X-COP lane corrects the equation object: the orthogonal term is inserted
only into reconstructed three-dimensional dark-halo density on the unchanged
hydrostatic-equilibrium right-hand side. The shared policy was frozen before
heldout scores, exact `f=0` recovery and deterministic replay passed, and all
three heldout cluster deltas were negative (`145.095308 → 140.737785`
chi-square; `3.0032%`).

The result remains limited. X-COP hydrostatic NFW profiles derive from the same
thermodynamic profile family used in the pressure score, the development
optimum reached the `f=1` grid boundary, and half-mass-matched Gaussian and
top-hat controls also improved all three clusters. The valid interpretation is
a public-profile direct-equation diagnostic, not independent raw-likelihood or
Plummer-specific proof.

## Durable conclusion

The evidence supports a reproducible redistribution effect in selected
diagnostic spaces, not a universal improvement. The independent Jeans
calibration rejected the nonzero adapter, and the separate Jeans-v2 adapter
failed on both untouched heldout galaxies. The combined record does not
currently require or identify a unique physical kernel or new cosmological
source term. The X-COP direct-equation lane adds a clean heldout directional
diagnostic, but generic-smoother and same-profile-family boundaries remain.
