# Equation insertions

The same operator grammar was placed into several established formulas. These are implementation locations, not independent confirmations.

## Poisson source-density lane

Baseline:

$$\nabla^2\Phi=4\pi G(\rho_b+\rho_{\rm gas}+\rho_{\rm halo}).$$

Augmented halo-only source:

$$
\nabla^2\Phi=4\pi G\left[\rho_b+\rho_{\rm gas}+\rho_{\rm halo}
+f_\perp(K_d*\rho_{\rm halo}-\rho_{\rm halo})\right].
$$

`X = rho_halo` only. BCG, gas, total convergence, and cumulative projected mass are not smoothed in the valid B2 implementation.

## Lensing convergence lane

$$
\kappa_{\rm base}=\kappa_b+\kappa_{\rm gas}+\kappa_{\rm halo},
$$

$$
\kappa_{\rm aug}=\kappa_b+\kappa_{\rm gas}
+(1-f_\perp)\kappa_{\rm halo}+f_\perp(P_d*\kappa_{\rm halo}).
$$

The HFF map-transfer diagnostic instead used a named target-team map as `X` and compared it with two other public model-team products; that is a model-product consistency test, not a decomposed physical halo likelihood.

## NFW / halo-profile lane

$$
\rho_{\rm aug}(r)=(1-f_\perp)\rho_{\rm NFW}(r)+f_\perp(K_d*\rho_{\rm NFW})(r).
$$

The SIDM Concerto runs compare this augmented CDM/NFW profile with a matched public parametric cored/SIDM reference. Since any low-pass operator removes a cusp, the direction is mechanically favorable; matched controls are essential.

## Jeans lane

The standard spherical Jeans equation is retained:

$$
\frac{d(\nu\sigma_r^2)}{dr}+\frac{2\beta}{r}\nu\sigma_r^2
=-\nu\frac{G M(<r)}{r^2}.
$$

The dwarf-spheroidal adapter acts only on the three-dimensional NFW halo density:

$$
d_g=\eta r_{1/2,g},
\qquad
\rho_{h,\rm aug}=(1-f)\rho_{\rm NFW}+f(K_{d_g}*\rho_{\rm NFW}),
$$

$$
M_{\rm aug}(<r)=M_\star(<r)+4\pi\int_0^r \rho_{h,\rm aug}(r')r'^2dr'.
$$

No separate free residual map is added, and the stellar tracer/mass is not convolved. Development calibration selected `f=0`; the forced nonzero diagnostic was slightly adverse on both heldout galaxies. Full details are in [`JEANS_DSPH_ADAPTER.md`](JEANS_DSPH_ADAPTER.md).

### Jeans-v2 response-orthogonal diagnostic

Jeans-v2 uses the same halo-only smoothing only to generate a raw response,
then removes the part locally degenerate with fitted baseline nuisances:

$$
\delta\boldsymbol\sigma_{\rm raw}
=\boldsymbol\sigma_{\rm Jeans}[M_\star+M_{\rm smoothed}]
-\boldsymbol\sigma_{\rm base},
$$

$$
\delta\boldsymbol\sigma_\perp
=W^{-1/2}(I-P_{W^{1/2}J})W^{1/2}
\delta\boldsymbol\sigma_{\rm raw},
\qquad
\boldsymbol\sigma_{\rm v2}
=\boldsymbol\sigma_{\rm base}+a_\perp\delta\boldsymbol\sigma_\perp.
$$

This is an empirical equation-response adapter, not a new density or source
law. The development-selected response worsened both untouched heldout
galaxies. Full details are in
[`JEANS_DSPH_RESPONSE_ADAPTER_V2.md`](JEANS_DSPH_RESPONSE_ADAPTER_V2.md).

## SPARC circular-velocity lane

For a SPARC galaxy, the fixed baryonic contribution is

$$
V_{\rm bar}^2(R)=V_{\rm gas}|V_{\rm gas}|
+0.5V_{\rm disk}|V_{\rm disk}|
+0.7V_{\rm bulge}|V_{\rm bulge}|.
$$

The per-galaxy baseline is

$$
V_{\rm base}^2(R)=V_{\rm bar}^2(R)
+\frac{G M_{\rm NFW}(<R;V_{200},c)}{R}.
$$

The shared equation adapter ties the 3D-kernel scale to the measured disk
scale length:

$$
d_g=\eta R_{{\rm disk},g},
\qquad
\rho_{{\rm aug},g}=(1-f)\rho_{{\rm NFW},g}
+f(K_{d_g}*\rho_{{\rm NFW},g}),
$$

$$
V_{\rm aug}^2(R)=V_{\rm bar}^2(R)+\frac{G M_{\rm aug}(<R)}{R}.
$$

The development-selected shared policy was `f = 1.0`, `eta = 0.125`, frozen
before heldout evaluation. It acts on halo-only 3D density. Each galaxy still
receives its own baseline NFW nuisance fit, so this lane tests transfer of the
shared adapter rather than clean end-to-end prediction.

## Program C Friedmann/background-fluid lane — a different term

$$
H^2(z)=H_0^2\left[\Omega_m(1+z)^3+\Omega_\perp(1+z)^q
+1-\Omega_m-\Omega_\perp\right].
$$

This represents `rho_perp(a) = rho_perp,0 a^-q`, with `w_perp = -1 + q/3`. It is not the cluster redistribution operator and is reported separately. The stored H(z) smoke found essentially no chi-square gain and worse information criteria.

## Einstein equation — container/design only

$$
G_{\mu\nu}+\Lambda g_{\mu\nu}=8\pi G\left(T^{\rm known}_{\mu\nu}+T^{\perp,\rm eff}_{\mu\nu}\right).
$$

A valid covariant implementation must conserve total stress-energy and reduce to the frozen weak-field operator. This repository does not claim that a complete covariant `T_perp_eff` was implemented or validated. The Einstein equation remains a formal container/design lane.
