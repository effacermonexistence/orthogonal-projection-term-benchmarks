# External data

No third-party data files are committed. Download the source products described in [`docs/DATA_PROVENANCE.md`](../docs/DATA_PROVENANCE.md), verify their checksums, and pass local paths to the reproduction adapters.

For the SPARC lane, use `data/sparc/Rotmod_LTG.zip` and
`data/sparc/SPARC_Lelli2016c.mrt`; the exact commands and expected hashes are in
[`scripts/sparc/README.md`](../scripts/sparc/README.md).

For the dwarf-spheroidal Jeans lane, download the CDS/VizieR
`J/AJ/137/3100` `ReadMe` and `table2.dat` through `table5.dat`; commands and
expected hashes are in [`scripts/jeans/README.md`](../scripts/jeans/README.md).

Jeans-v2 additionally uses the Spencer et al. (2018) CDS/VizieR
`J/AJ/156/257` Draco and Ursa Minor multi-epoch tables and McConnachie (2012)
`J/AJ/144/4` structural metadata. Exact source identifiers and hashes are in
[`docs/DATA_PROVENANCE.md`](../docs/DATA_PROVENANCE.md); raw catalogs are not
redistributed.
