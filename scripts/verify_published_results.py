#!/usr/bin/env python3
from __future__ import annotations
import hashlib, json, pathlib, re, sys
ROOT=pathlib.Path(__file__).resolve().parents[1]
def close(a,b,tol=1e-10):
    if abs(a-b)>tol*max(1.0,abs(a),abs(b)): raise AssertionError(f'{a} != {b}')
def load(rel): return json.loads((ROOT/rel).read_text())
def verify_delta(base,aug,delta,reduction):
    close(aug-base,delta); close(100*(base-aug)/base,reduction)
def verify_sparc():
    held=load('results/sparc_rotation_curve_heldout.json')
    dev=load('results/sparc_rotation_curve_dev_grid.json')
    policy=load('results/sparc_rotation_curve_frozen_policy.json')
    sample=load('results/sparc_rotation_curve_sample_manifest.json')
    receipt=load('results/sparc_rotation_curve_run_receipt.json')
    verification=load('results/sparc_rotation_curve_verification.json')
    public_reproduction=load('results/sparc_rotation_curve_public_reproduction_check.json')
    assert not set(sample['dev']).intersection(sample['heldout'])
    assert held['heldout_names']==sample['heldout']
    assert held['forced_nonzero_policy']['f']==policy['forced_nonzero_optimum']['f']==1.0
    assert held['forced_nonzero_policy']['eta']==policy['forced_nonzero_optimum']['eta']==0.125
    assert dev['heldout_accessed'] is False
    stable=[row for row in held['rows'] if row['baseline_stable']]
    assert len(stable)==6
    mapping={
      'forced_plummer':'forced_plummer',
      'forced_gaussian':'forced_gaussian',
      'forced_top_hat':'forced_top_hat',
      'safe_plummer':'safe_plummer',
    }
    for aggregate_key,row_key in mapping.items():
        aggregate=held['aggregates'][aggregate_key]
        base=sum(row['baseline_chi2'] for row in stable)
        candidate=sum(row[row_key]['chi2'] for row in stable)
        verify_delta(base,candidate,aggregate['raw_delta_chi2'],aggregate['residual_reduction_pct'])
        close(base,aggregate['baseline_total_chi2'])
        close(candidate,aggregate['candidate_total_chi2'])
        assert aggregate['improved_count']==sum(row[row_key]['delta_chi2']<0 for row in stable)
        assert aggregate['worsened_count']==sum(row[row_key]['delta_chi2']>0 for row in stable)
        for row in stable:
            r=row[row_key]
            verify_delta(row['baseline_chi2'],r['chi2'],r['delta_chi2'],r['residual_reduction_pct'])
            assert r['f0_max_abs']==0.0
            assert abs(r['raw_mass_leak_fraction'])<=0.02
            assert abs(r['mass_leak_fraction'])<=1e-12
    plummer=held['aggregates']['forced_plummer']
    close(plummer['raw_delta_chi2'],-9.256213018221956)
    close(plummer['residual_reduction_pct'],4.432098539050158)
    assert plummer['improved_count']==5 and plummer['worsened_count']==1
    assert verification['status']=='PASS' and verification['byte_identical_replay'] is True
    assert verification['dev_heldout_overlap']==0
    assert receipt['heldout_aggregate']==plummer
    assert receipt['claim_boundary']==held['claim_boundary']
    assert public_reproduction['status']=='PASS'
    assert public_reproduction['scope']=='PUBLIC_REPRODUCTION_NUMERICAL_PARITY_ONLY'
    assert public_reproduction['heldout_numeric_match']['aggregate']==plummer
def verify_jeans():
    held=load('results/jeans_dsph_heldout.json')
    dev=load('results/jeans_dsph_dev_grid.json')
    policy=load('results/jeans_dsph_frozen_policy.json')
    sample=load('results/jeans_dsph_sample_manifest.json')
    receipt=load('results/jeans_dsph_run_receipt.json')
    verification=load('results/jeans_dsph_verification.json')
    failures=load('results/jeans_dsph_failure_ledger.json')
    assert not set(sample['dev']).intersection(sample['heldout'])
    assert sample['dev']==['Sextans','Fornax']
    assert sample['heldout']==['Sculptor','Carina']
    assert held['heldout_names']==sample['heldout']
    assert dev['heldout_accessed'] is False
    assert policy['heldout_scores_accessed'] is False
    assert held['safe_policy']['f']==policy['safe_optimum']['f']==0.0
    assert held['forced_nonzero_policy']['f']==policy['forced_nonzero_optimum']['f']==0.05
    assert held['forced_nonzero_policy']['eta']==policy['forced_nonzero_optimum']['eta']==0.03125
    assert sample['dispersion_profiles']['Carina']['member_count']==746
    assert sample['dispersion_profiles']['Fornax']['member_count']==2279
    assert sample['dispersion_profiles']['Sculptor']['member_count']==1349
    assert sample['dispersion_profiles']['Sextans']['member_count']==397
    rows=held['rows']
    assert len(rows)==2 and all(row['baseline_stable'] for row in rows)
    for key in ('safe_plummer','forced_plummer','forced_gaussian','forced_top_hat'):
        aggregate=held['aggregates'][key]
        base=sum(row['baseline_chi2'] for row in rows)
        candidate=sum(row[key]['chi2'] for row in rows)
        verify_delta(base,candidate,aggregate['raw_delta_chi2'],aggregate['residual_reduction_pct'])
        close(base,aggregate['baseline_total_chi2'])
        close(candidate,aggregate['candidate_total_chi2'])
        assert aggregate['improved_count']==sum(row[key]['delta_chi2']<0 for row in rows)
        assert aggregate['worsened_count']==sum(row[key]['delta_chi2']>0 for row in rows)
        for row in rows:
            result=row[key]
            verify_delta(row['baseline_chi2'],result['chi2'],result['delta_chi2'],result['residual_reduction_pct'])
            assert result['f0_max_abs_kms']==0.0
            assert abs(result['raw_mass_leak_fraction'])<=0.02
            assert abs(result['mass_leak_fraction'])<=1e-12
    safe=held['aggregates']['safe_plummer']
    forced=held['aggregates']['forced_plummer']
    close(safe['raw_delta_chi2'],0.0)
    close(forced['raw_delta_chi2'],0.00190530699818936)
    close(forced['residual_reduction_pct'],-0.005389404945401978)
    assert forced['improved_count']==0 and forced['worsened_count']==2
    assert verification['status']=='PASS'
    assert verification['checks']['dev_replay_byte_identical'] is True
    assert verification['checks']['heldout_replay_byte_identical'] is True
    assert receipt['status']=='COMPLETE_NEGATIVE_RESULT'
    assert receipt['result_label']=='NO_ADAPTER_UPLIFT_SAFE_FLOOR_SELECTED'
    assert receipt['heldout_aggregates']==held['aggregates']
    assert receipt['claim_boundary']==held['claim_boundary']
    assert len(failures['failures'])==3
def main():
    hff=load('results/hff_six_cluster_transfer.json')
    for row in hff['rows']:
        for key in ('plummer_like_2d','gaussian_2d','top_hat_2d'):
            r=row[key]; verify_delta(row['baseline_mean_mse'],r['augmented_mean_mse'],r['raw_delta_mse'],r['residual_reduction_pct'])
    b2=load('results/as1063_b2_true_density.json'); verify_delta(b2['base_score']['chi_total'],b2['augmented_score']['chi_total'],b2['raw_delta_chi_total'],b2['residual_reduction_pct'])
    for rel in ('results/as1063_b2_matched_controls.json','results/sidm_halo000_3d.json','results/sidm_halo352_fresh_3d.json'):
        x=load(rel); base=x['base_chi_total']
        for r in x['kernels'].values(): verify_delta(base,r['chi_total'],r['raw_delta_chi_total'],r['residual_reduction_pct'])
    verify_sparc()
    verify_jeans()
    forbidden=[re.compile('/'+'Users/'),re.compile(r'sk-(?:proj-)?[A-Za-z0-9_-]{16,}'),re.compile(r'BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY')]
    skipped={'.git','.venv','__pycache__','.pytest_cache','build','dist'}
    for p in ROOT.rglob('*'):
        if not p.is_file() or skipped.intersection(p.parts) or any(part.endswith('.egg-info') for part in p.parts): continue
        try: text=p.read_text()
        except UnicodeDecodeError: continue
        for pat in forbidden:
            if pat.search(text): raise AssertionError(f'forbidden content {pat.pattern!r} in {p.relative_to(ROOT)}')
    manifest=load('RELEASE_MANIFEST.json')
    for rel,expected in manifest['files'].items():
        actual=hashlib.sha256((ROOT/rel).read_bytes()).hexdigest()
        if actual!=expected: raise AssertionError(f'hash mismatch: {rel}')
    print(json.dumps({'status':'PASS','arithmetic':'PASS','local_path_scan':'PASS','secret_scan':'PASS','manifest_files':len(manifest['files'])},indent=2))
    return 0
if __name__=='__main__': raise SystemExit(main())
