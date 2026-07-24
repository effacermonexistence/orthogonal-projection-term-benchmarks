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

The standard spherical Jeans calculation is retained, but its mass source is derived from the corrected density:

$$
M_{\rm aug}(<r)=4\pi\int_0^r \rho_{\rm aug}(r')r'^2dr'.
$$

No separate free residual map is added.

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
