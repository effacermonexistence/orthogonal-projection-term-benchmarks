#!/usr/bin/env python3
from __future__ import annotations
import hashlib, json, pathlib, re, sys
ROOT=pathlib.Path(__file__).resolve().parents[1]
def close(a,b,tol=1e-10):
    if abs(a-b)>tol*max(1.0,abs(a),abs(b)): raise AssertionError(f'{a} != {b}')
def load(rel): return json.loads((ROOT/rel).read_text())
def verify_delta(base,aug,delta,reduction):
    close(aug-base,delta); close(100*(base-aug)/base,reduction)
def main():
    hff=load('results/hff_six_cluster_transfer.json')
    for row in hff['rows']:
        for key in ('plummer_like_2d','gaussian_2d','top_hat_2d'):
            r=row[key]; verify_delta(row['baseline_mean_mse'],r['augmented_mean_mse'],r['raw_delta_mse'],r['residual_reduction_pct'])
    b2=load('results/as1063_b2_true_density.json'); verify_delta(b2['base_score']['chi_total'],b2['augmented_score']['chi_total'],b2['raw_delta_chi_total'],b2['residual_reduction_pct'])
    for rel in ('results/as1063_b2_matched_controls.json','results/sidm_halo000_3d.json','results/sidm_halo352_fresh_3d.json'):
        x=load(rel); base=x['base_chi_total']
        for r in x['kernels'].values(): verify_delta(base,r['chi_total'],r['raw_delta_chi_total'],r['residual_reduction_pct'])
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
