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
def test_sparc_shared_adapter_numbers_and_boundary():
    x=json.loads((ROOT/'results/sparc_rotation_curve_heldout.json').read_text())
    a=x['aggregates']['forced_plummer']
    assert round(a['raw_delta_chi2'],6)==-9.256213
    assert round(a['residual_reduction_pct'],3)==4.432
    assert a['improved_count']==5
    assert a['worsened_count']==1
    assert x['forced_nonzero_policy']['f']==1.0
    assert x['forced_nonzero_policy']['eta']==0.125
    assert x['claim_allowed'] is False
def test_sparc_generic_controls_are_visible():
    x=json.loads((ROOT/'results/sparc_rotation_curve_heldout.json').read_text())
    p=x['aggregates']['forced_plummer']['candidate_total_chi2']
    g=x['aggregates']['forced_gaussian']['candidate_total_chi2']
    t=x['aggregates']['forced_top_hat']['candidate_total_chi2']
    assert p < g and p < t
    assert x['aggregates']['forced_gaussian']['improved_count']==5
    assert x['aggregates']['forced_top_hat']['improved_count']==5
def test_sparc_public_reproduction_check_is_bounded():
    x=json.loads((ROOT/'results/sparc_rotation_curve_public_reproduction_check.json').read_text())
    assert x['status']=='PASS'
    assert x['scope']=='PUBLIC_REPRODUCTION_NUMERICAL_PARITY_ONLY'
    assert 'not a new heldout run' in x['proof_boundary']
def test_jeans_calibration_selected_safe_floor():
    x=json.loads((ROOT/'results/jeans_dsph_heldout.json').read_text())
    assert x['safe_policy']['f']==0.0
    assert x['aggregates']['safe_plummer']['raw_delta_chi2']==0.0
    assert x['claim_allowed'] is False
def test_jeans_forced_nonzero_result_is_negative():
    x=json.loads((ROOT/'results/jeans_dsph_heldout.json').read_text())
    a=x['aggregates']['forced_plummer']
    assert round(a['raw_delta_chi2'],9)==0.001905307
    assert round(a['residual_reduction_pct'],6)==-0.005389
    assert a['improved_count']==0
    assert a['worsened_count']==2
    assert a['downlift'] is True
def test_jeans_replay_and_numerical_gates_passed():
    x=json.loads((ROOT/'results/jeans_dsph_verification.json').read_text())
    assert x['status']=='PASS'
    assert x['checks']['dev_replay_byte_identical'] is True
    assert x['checks']['heldout_replay_byte_identical'] is True
    assert x['checks']['all_f0_exact'] is True
    assert x['checks']['all_mass_corrections_within_gate'] is True
def test_jeans_v2_untouched_heldout_is_negative():
    x=json.loads((ROOT/'results/jeans_dsph_v2_heldout.json').read_text())
    a=x['aggregates']['safe_plummer']
    assert x['heldout_names']==['Draco','Ursa Minor']
    assert round(a['baseline_total_chi2'],6)==22.835649
    assert round(a['candidate_total_chi2'],6)==24.085741
    assert round(a['raw_delta_chi2'],6)==1.250092
    assert round(a['residual_reduction_pct'],3)==-5.474
    assert a['improved_count']==0
    assert a['worsened_count']==2
    assert a['downlift'] is True
    assert x['claim_allowed'] is False
def test_jeans_v2_policy_was_frozen_and_bounded():
    x=json.loads((ROOT/'results/jeans_dsph_v2_frozen_policy.json').read_text())
    assert x['status']=='FROZEN_BEFORE_HELDOUT_BASELINE_OR_CANDIDATE_SCORING'
    assert x['safe_optimum']['eta']==0.5
    assert x['safe_optimum']['amplitude']==2.0
    assert x['safe_optimum']['amplitude_solution']['upper_bound_hit'] is True
    assert x['no_heldout_parameter_update'] is True
    assert x['no_heldout_row_fallback'] is True
def test_jeans_v2_public_replay_and_audit_pass():
    replay=json.loads((ROOT/'results/jeans_dsph_v2_replay_receipt.json').read_text())
    audit=json.loads((ROOT/'results/jeans_dsph_v2_verification.json').read_text())
    assert replay['status']=='PASS'
    assert replay['dev_byte_identical'] is True
    assert replay['heldout_byte_identical'] is True
    assert audit['verdict']=='PASS_NEGATIVE_RESULT_PRESERVED'
    assert audit['check_count']==27
    assert audit['failed_checks']==[]

def test_jeans_corrective_direct_source_is_tiny_negative_direction():
    x=json.loads((ROOT/'results/jeans_dsph_formal_corrective_evaluation.json').read_text())
    a=x['aggregates']['direct_nonzero_plummer']
    assert x['response_projection_used'] is False
    assert x['proof_mode']=='POST_EXPOSURE_CORRECTIVE_FORMAL_SOURCE_REPRODUCTION'
    assert round(a['raw_delta_chi2'],12)==round(-0.0011593988829652346,12)
    assert round(a['residual_reduction_pct'],9)==round(0.005077144705320756,9)
    assert a['improved_count']==2 and a['worsened_count']==0
    assert x['claim_allowed'] is False

def test_jeans_corrective_safe_policy_and_audit_boundary():
    policy=json.loads((ROOT/'results/jeans_dsph_formal_corrective_frozen_policy.json').read_text())
    audit=json.loads((ROOT/'results/jeans_dsph_formal_corrective_audit.json').read_text())
    assert policy['safe_optimum']['f']==0.0
    assert policy['direct_nonzero_optimum']['f']==0.05
    assert policy['direct_nonzero_optimum']['eta']==0.03125
    assert audit['status']=='PASS'
    assert audit['audit_label']=='CORRECT_FORMAL_SOURCE_DIRECTIONAL_DELTA_NEGATIVE_BUT_MATERIALITY_NOT_ESTABLISHED'
    assert len(audit['checks'])==61 and all(x['pass'] for x in audit['checks'])

def test_jeans_corrective_public_reproduction_parity():
    x=json.loads((ROOT/'results/jeans_dsph_formal_corrective_public_reproduction_check.json').read_text())
    assert x['status']=='PASS_NUMERICAL_PARITY'
    assert x['scope']=='PUBLIC_REPRODUCTION_NUMERICAL_PARITY_ONLY'
    assert x['policy_identity_preserved'] is True
    assert x['direction_counts_preserved'] is True
    assert x['delta_signs_preserved'] is True
    assert x['max_raw_delta_chi2_difference']==0.0
