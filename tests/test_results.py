import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def test_fresh_halo352_numbers():
    x=json.loads((ROOT/'results/sidm_halo352_fresh_3d.json').read_text())
    assert round(x['kernels']['plummer_3d']['residual_reduction_pct'],3)==41.000
    assert x['kernels']['gaussian_3d']['chi_total'] < x['kernels']['plummer_3d']['chi_total']
    assert x['kernels']['tophat_3d']['chi_total'] < x['kernels']['plummer_3d']['chi_total']
def test_hff_controls_are_not_hidden():
    x=json.loads((ROOT/'results/hff_six_cluster_transfer.json').read_text())
    assert x['summary']['plummer_improved']==6
    assert x['summary']['plummer_better_than_gaussian_clusters']==1
    assert x['summary']['plummer_better_than_tophat_clusters']==1
