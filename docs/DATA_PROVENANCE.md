# Data provenance

Raw third-party datasets are not committed. This repository stores URLs, source versions, and cryptographic checksums sufficient to identify the inputs used.

## AS1063 Beauchesne public Lenstool model

- Repository: https://github.com/njzifjoiez/AS1063-model-Beauchesne-2023
- Frozen commit: `f53a37f96d1122b1524d4b0b9caf1031311b9026`
- `AS1063-model.zip` SHA-256: `0f57ff5c735b75a7b84d6316c741790f639d1c6b3aabd1fcdfa679162d042fa5`
- Use: cluster-scale dPIE halo components only for the B2 density diagnostic.

## Hubble Frontier Fields lens-model products

- Archive root: https://archive.stsci.edu/pub/hlsp/frontier/
- Products: public `kappa` maps from CATS, GLAFIC, and Williams teams for Abell 2744, Abell 370, Abell S1063, MACS J0416, MACS J0717, and MACS J1149.
- Exact per-file SHA-256 values are embedded in [`results/hff_six_cluster_transfer.json`](../results/hff_six_cluster_transfer.json).
- No FITS products are redistributed here.

## SIDM Concerto parametric release

- DOI: https://doi.org/10.5281/zenodo.14933624
- Zenodo record: https://zenodo.org/records/14933624
- Halo000 table SHA-256: `27a7ebf05e98dff1b9c6144777e957c2352f3c073a71fd25422e5eef8eb473ae`
- Halo000 archive SHA-256: `af539d799bc1a340072a0300afa5784209aa243c71ad332ba0412bf0a6de0dbb`
- Halo352 table SHA-256: `d8149f2883dd06c6e4fab464b712391b46c2a3d583a5f8953348851a6e4af380`
- Halo352 archive SHA-256: `950a5ca7840b1e8b003008fc7ac1024f2b40a487a3d008ce040b923cf7ec1430`
- Halo352 official archive MD5: `100863ce7e3284c5b39107e6e8a9f285`

## H(z) compilation

- Compilation reference: https://arxiv.org/abs/2111.08289
- Source repository: https://github.com/reggiebernardo/datasets
- Source file: https://raw.githubusercontent.com/reggiebernardo/datasets/main/Hdz_2020_CConly.txt
- SHA-256: `bd36beac5c36d161437ee32d9a597195544a3a5c092e74bb58fca73998778f3b`

## SPARC galaxy rotation curves

- Dataset: SPARC v1, 175 disk galaxies.
- Authors: Federico Lelli, Stacy McGaugh, and James Schombert.
- Master paper: https://doi.org/10.3847/0004-6256/152/6/157
- Official project page: https://astroweb.case.edu/SPARC/
- Archived dataset DOI: https://doi.org/10.5281/zenodo.16284118
- `Rotmod_LTG.zip` download:
  https://zenodo.org/records/16284118/files/Rotmod_LTG.zip?download=1
- `Rotmod_LTG.zip` SHA-256:
  `0a80cc90714828cc28b7dd57923576714d209f2490328c087c4a4ad607faf588`
- `Rotmod_LTG.zip` official MD5: `e4c8b92766026770ed35e5889064e12b`
- `SPARC_Lelli2016c.mrt` download:
  https://zenodo.org/records/16284118/files/SPARC_Lelli2016c.mrt?download=1
- `SPARC_Lelli2016c.mrt` SHA-256:
  `5aa0501f6b0d881fa579030e315e7b5b6ef561a5bd3a07472f9929c7e5728243`
- `SPARC_Lelli2016c.mrt` official MD5:
  `6181df386bfc05868a3700c196e800da`
- Use: public rotation-curve observations, baryonic velocity components, and
  galaxy metadata for the shared equation-adapter dev/heldout diagnostic.
- The original source files are not redistributed in this repository.

## Integrity boundary

Checksums identify byte-level inputs; they do not elevate a public model product into raw observational data. Each result file states its evidence class.
