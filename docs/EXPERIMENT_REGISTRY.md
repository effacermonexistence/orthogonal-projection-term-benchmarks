# Experiment registry and independence map

The registry contains **nine experimental records**, not nine independent confirmations.

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

## Development chain

The initial five-cluster likelihood was reused across M0/M1/M2/M3, Program EA, and several canonical-channel views. Renaming an objective or slicing channels does not create a new empirical unit. The public registry keeps those related rows together.

## Direction versus specificity

Two questions are deliberately separated:

1. **Directional:** did the frozen augmented profile reduce the chosen residual?
2. **Specificity:** did the Plummer kernel beat half-mass-matched Gaussian and top-hat controls under the frozen comparison rule?

The strongest fresh 3D run passed the first question and failed the second. Therefore the current durable result is a generic redistribution effect under the selected diagnostic, not Plummer-specific evidence.

## SPARC shared-adapter lane

SPARC adds a new observational domain and freezes one shared `f/eta` policy after development before evaluating the heldout galaxy identities. This is stronger than replaying the same development rows, but the heldout boundary does not cover each galaxy's baseline NFW nuisance fit. One of seven heldout baselines hit a bound and is retained as an excluded row. The valid public label is `PUBLIC_DATA_DEV_OPTIMIZATION_PLUS_HELDOUT_SHARED_ADAPTER_DIAGNOSTIC`.
