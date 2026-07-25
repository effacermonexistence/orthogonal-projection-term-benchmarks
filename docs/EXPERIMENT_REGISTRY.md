# Experiment registry and independence map

The registry contains **eleven experimental records**, not eleven independent confirmations.

| Record | Stored units | Independence status | Result class |
|---|---:|---|---|
| N13 development chain | 5 clusters / one reused likelihood | Development-only | M1 within null; M2 absorbs residual |
| Program C H(z) | 31 H(z) rows | Separate dataset, different term | No real uplift |
| Program EA weak-field/lensing | 5 clusters | Same N13 sample | Same-sample diagnostic |
| Canonical equation channels | 6 named channels | Overlapping objectives; not 6 datasets | Placement/channel audit |
| AS1063 true-density B2 | 1 public model pair | Model-component diagnostic | Directional reduction; specificity unresolved |
| HFF map transfer | 6 clusters | Six targets, shared teams/systematics | Generic low-pass effect |
| SIDM Concerto Halo000 | 1 public simulation-parametric target | New target | Direction pass; specificity fail |
| SIDM Concerto Halo352 | 1 score-blind fresh target | New target | Direction pass; specificity fail |
| SPARC rotation-curve adapter | 14 dev / 7 heldout; 6 stable heldout | New public-data domain; shared adapter held out, per-galaxy nuisances fitted | 4.432% aggregate heldout reduction; diagnostic only |
| Dwarf-spheroidal spherical-Jeans adapter | 2 dev / 2 heldout | New public-data domain; shared adapter held out, per-galaxy nuisances fitted | Safe policy selected `f=0`; forced term slightly worsened both heldout galaxies |
| Jeans-v2 nuisance-orthogonal response adapter | 4 dev / 2 untouched heldout | Different public heldout catalog and galaxy identities; shared `eta/a_perp` frozen; per-galaxy nuisances fitted | Frozen Plummer response worsened Draco and Ursa Minor; no generalization |

## Development chain

The initial five-cluster likelihood was reused across M0/M1/M2/M3, Program EA, and several canonical-channel views. Renaming an objective or slicing channels does not create a new empirical unit. The public registry keeps those related rows together.

## Direction versus specificity

Two questions are deliberately separated:

1. **Directional:** did the frozen augmented profile reduce the chosen residual?
2. **Specificity:** did the Plummer kernel beat half-mass-matched Gaussian and top-hat controls under the frozen comparison rule?

The strongest fresh 3D run passed the first question and failed the second. Therefore the current durable result is a generic redistribution effect under the selected diagnostic, not Plummer-specific evidence.

## SPARC shared-adapter lane

SPARC adds a new observational domain and freezes one shared `f/eta` policy after development before evaluating the heldout galaxy identities. This is stronger than replaying the same development rows, but the heldout boundary does not cover each galaxy's baseline NFW nuisance fit. One of seven heldout baselines hit a bound and is retained as an excluded row. The valid public label is `PUBLIC_DATA_DEV_OPTIMIZATION_PLUS_HELDOUT_SHARED_ADAPTER_DIAGNOSTIC`.

## Dwarf-spheroidal Jeans lane

The Walker et al. public stellar-velocity catalogs add another equation and data domain. Sextans and Fornax calibrated a shared `f/eta` grid; Sculptor and Carina were held out from shared-policy selection. Calibration selected `f=0`, while the separately frozen forced-nonzero Plummer diagnostic produced `delta chi-square = +0.001905307` and worsened both heldout galaxies. This is a complete negative result under the label `NO_ADAPTER_UPLIFT_SAFE_FLOOR_SELECTED`. As in SPARC, each heldout object's own baseline NFW and anisotropy nuisances were fitted, so the lane is not clean end-to-end prediction.

## Jeans-v2 response-orthogonal lane

Jeans-v2 retains all four previously inspected Walker galaxies as development
and evaluates a different response construction on Draco and Ursa Minor from
Spencer et al. (2018), with structural metadata from McConnachie (2012).
The shared `eta=0.5`, `a_perp=2.0` policy was frozen before any heldout model
score. The Plummer response changed heldout chi-square from 22.835649 to
24.085741 (`delta = +1.250092`; residual reduction `-5.474%`) and worsened
both galaxies. Matched Gaussian and top-hat responses also worsened both.
The result label is
`UNTOUCHED_GALAXY_HELDOUT_DOWNLIFT_NO_GENERALIZATION`.

This is a stronger heldout boundary than Jeans-v1 for shared adapter transfer,
but each heldout galaxy still has a fitted NFW/anisotropy baseline. The result
is therefore a clean negative adapter-generalization diagnostic, not clean
end-to-end prediction.
