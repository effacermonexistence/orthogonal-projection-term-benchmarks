# Jeans-v2 nuisance-orthogonal response adapter

## Result

Jeans-v2 was designed after Jeans-v1 rejected the direct density adapter. It does **not** overwrite that earlier negative result. The new adapter was calibrated on four previously inspected development galaxies and then frozen before any model score was computed for Draco or Ursa Minor from a different public catalog.

The development-calibrated policy worsened both untouched heldout galaxies:

- baseline total chi-square: `22.835648837370`;
- frozen Plummer candidate: `24.085741154812`;
- raw delta chi-square: `+1.250092317442`;
- residual reduction: `-5.474302%`;
- improved / worsened heldout galaxies: `0 / 2`.

**Result label:** `UNTOUCHED_GALAXY_HELDOUT_DOWNLIFT_NO_GENERALIZATION`.

This is a clean negative generalization result. It is not uplift, physical-law evidence, or Plummer-specific evidence.

## Why v2 is a different adapter

The baseline remains the spherical Jeans equation,

$$
\frac{d(\nu\sigma_r^2)}{dr}+\frac{2\beta}{r}\nu\sigma_r^2
=-\nu\frac{G M_{\rm base}(<r)}{r^2},
\qquad
M_{\rm base}=M_{\star,\mathrm{Plummer}}+M_{\mathrm{NFW}}.
$$

For a trial shared scale `d_g = eta r_half,g`, the halo-only three-dimensional Plummer redistribution first generates a raw line-of-sight dispersion response,

$$
\delta\boldsymbol\sigma_{\rm raw}
=
\boldsymbol\sigma_{\rm Jeans}[M_\star+M_{\rm smoothed}]
-
\boldsymbol\sigma_{\rm base}.
$$

Let `J` be the finite-difference Jacobian of the baseline prediction with respect to the fitted nuisance vector `(log10 rho_s, log10 r_s, beta)`, and let `W` be the inverse observation-error covariance. Jeans-v2 removes the component of the raw response that lies in the local weighted nuisance tangent:

$$
\delta\boldsymbol\sigma_\perp
=
W^{-1/2}
\left(I-P_{W^{1/2}J}\right)
W^{1/2}
\delta\boldsymbol\sigma_{\rm raw}.
$$

The candidate prediction is

$$
\boldsymbol\sigma_{\rm v2}
=
\boldsymbol\sigma_{\rm base}
+a_\perp\delta\boldsymbol\sigma_\perp,
\qquad a_\perp\ge 0.
$$

This construction is an **empirical equation-response adapter**. It is not asserted to be a covariant stress-energy source, a new density law, or a physical derivation.

## Locked development and heldout split

| Galaxy | Public catalog | Members used | Bins | Role |
|---|---|---:|---:|---|
| Carina | Walker et al. 2009, `J/AJ/137/3100` | 746 | 14 | development |
| Fornax | Walker et al. 2009, `J/AJ/137/3100` | 2,279 | 20 | development |
| Sculptor | Walker et al. 2009, `J/AJ/137/3100` | 1,349 | 18 | development |
| Sextans | Walker et al. 2009, `J/AJ/137/3100` | 397 | 10 | development |
| Draco | Spencer et al. 2018, `J/AJ/156/257` | 311 | 9 | untouched heldout |
| Ursa Minor | Spencer et al. 2018, `J/AJ/156/257` | 266 | 8 | untouched heldout |

The heldout catalog supplied 341 Draco stars / 1,204 observations and 284 Ursa Minor stars / 875 observations. A predeclared constant-velocity chi-square rule excluded 30 and 18 binary candidates respectively before profile construction. Structural metadata came from McConnachie (2012), `J/AJ/144/4`.

Galaxy overlap was zero. Public raw catalogs were visible as source material, but heldout baseline and candidate scores were not computed before policy freeze.

## Development calibration

Frozen search space:

- `eta` in `{0.03125, 0.0625, 0.125, 0.25, 0.5, 1, 2, 4, 8}`;
- shared nonnegative `a_perp` analytically optimized and clipped to `[0, 2]`;
- objective: macro mean chi-square per bin across the four development galaxies;
- no candidate nuisance refit;
- no heldout row fallback or subset exclusion.

The development optimum was:

| Metric | Value |
|---|---:|
| `eta` | 0.5 |
| `a_perp` | 2.0 |
| unconstrained analytic amplitude | 2.917617693553 |
| baseline macro chi-square/bin | 0.786048234769 |
| candidate macro chi-square/bin | 0.761364854049 |
| development delta | -0.024683380720 |
| improved / worsened development galaxies | 2 / 2 |

The selected amplitude hit the declared upper bound. That is a limitation. The bound was not widened after observing heldout results.

## Frozen heldout result

| Kernel | Baseline chi-square | Candidate chi-square | Raw delta | Residual reduction | Improved / worsened |
|---|---:|---:|---:|---:|---:|
| 3D Plummer | 22.835648837370 | 24.085741154812 | +1.250092317442 | -5.474302% | 0 / 2 |
| half-mass-matched 3D Gaussian | 22.835648837370 | 24.052974040275 | +1.217325202905 | -5.330811% | 0 / 2 |
| half-mass-matched 3D top-hat | 22.835648837370 | 23.566904411206 | +0.731255573836 | -3.202254% | 0 / 2 |

| Galaxy | Baseline | Plummer candidate | Delta |
|---|---:|---:|---:|
| Draco | 13.087048478046 | 13.537068890508 | +0.450020412462 |
| Ursa Minor | 9.748600359324 | 10.548672264304 | +0.800071904980 |

All three frozen kernels worsened both heldout galaxies. There is no v2 generalization uplift to adopt.

## Execution and verification

- proof contract frozen before candidate generation;
- source selection frozen and content-addressed;
- OmarAGI R2 pre gate: `PASS`;
- selected R2 callable invoked and post gate: `PASS`;
- policy frozen before heldout baseline or candidate scoring;
- no heldout parameter update, row fallback, or subset exclusion;
- development replay: byte-identical;
- heldout replay: byte-identical;
- independent local audit script: `PASS_NEGATIVE_RESULT_PRESERVED` with 27 checks and zero failures; this is not an external peer-review claim;
- public-data source hashes verified;
- all heldout numerical gates passed.

The exact machine-readable artifacts are under `results/jeans_dsph_v2_*`. Public derivatives replace local paths with public source identifiers; scientific arrays and scores are unchanged.

## Proof boundary

The heldout boundary covers the shared `eta/a_perp` response rule and uses galaxy identities and a catalog source not used in development. Each heldout galaxy still fits its own baseline NFW and constant-anisotropy nuisances from its profile. This is therefore stronger than same-row development replay but remains an equation-adapter generalization diagnostic, not clean end-to-end prediction or physical proof.
