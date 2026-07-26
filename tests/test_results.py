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

def test_jeans_v2_is_excluded_from_canonical_method_tally():
    registry=json.loads((ROOT/'results/experiment_registry.json').read_text())
    rows={row['record_id']:row for row in registry['records']}
    v2=rows['DSPH_JEANS_V2_RESPONSE_ORTHOGONAL_ADAPTER']
    corrective=rows['DSPH_JEANS_DIRECT_FORMAL_SOURCE_CORRECTIVE']
    assert v2['status']=='OFF_OBJECT_RESPONSE_ADAPTER_NEGATIVE_NOT_CANONICAL_TERM_TEST'
    assert v2['method_relevance']=='EXCLUDED_FROM_CANONICAL_ORTHOGONAL_METHOD_TALLY'
    assert v2['superseded_for_canonical_object_question_by']==corrective['record_id']
    assert corrective['method_relevance']=='CANONICAL_DIRECT_SOURCE_CORRECTIVE_POST_EXPOSURE'

def test_method_object_identity_audit_passes():
    x=json.loads((ROOT/'results/downlift_object_identity_audit.json').read_text())
    assert x['status']=='PASS'
    rows={row['record_id']:row for row in x['records']}
    v1=rows['DSPH_SPHERICAL_JEANS_SHARED_ADAPTER']
    v2=rows['DSPH_JEANS_V2_RESPONSE_ORTHOGONAL_ADAPTER']
    corrected=rows['DSPH_JEANS_DIRECT_FORMAL_SOURCE_CORRECTIVE']
    assert v1['adopted_delta_chi2']==0.0
    assert v1['canonical_method_downlift_adopted'] is False
    assert v2['canonical_direct_source_test'] is False
    assert v2['raw_result_preserved'] is True
    assert corrected['response_projection_used'] is False
    assert corrected['direct_nonzero_delta_chi2']<0.0

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

def test_xcop_direct_hydrostatic_heldout_result():
    x=json.loads((ROOT/'results/xcop_hse_heldout.json').read_text())
    a=x['safe_aggregate']
    assert x['heldout']==['A644','A2029','A1795']
    assert x['overlap_count']==0
    assert x['safe_policy']['f']==1.0
    assert x['safe_policy']['eta']==0.01
    assert round(a['baseline_chi2_sum'],6)==145.095308
    assert round(a['augmented_chi2_sum'],6)==140.737785
    assert round(a['delta_chi2_sum'],6)==-4.357523
    assert a['improved_count']==3
    assert a['downlift_count']==0
    assert x['f0_recovery']['pass'] is True

def test_xcop_controls_and_audit_boundary():
    x=json.loads((ROOT/'results/xcop_hse_heldout.json').read_text())
    audit=json.loads((ROOT/'results/xcop_hse_adversarial_audit.json').read_text())
    p=x['safe_aggregate']['augmented_chi2_sum']
    g=x['generic_control_aggregates']['gaussian']['augmented_chi2_sum']
    t=x['generic_control_aggregates']['top_hat']['augmented_chi2_sum']
    assert p < g < t
    assert x['generic_control_aggregates']['gaussian']['improved_count']==3
    assert x['generic_control_aggregates']['top_hat']['improved_count']==3
    assert audit['status']=='PASS'
    assert audit['direct_formal_equation_label']=='PASS'
    assert audit['heldout_directional_label']=='DESCRIPTIVE_PASS_3_OF_3_NO_DOWNLIFT'
    assert audit['plummer_specificity_label']=='AGGREGATE_ADVANTAGE_OVER_MATCHED_CONTROLS_NOT_ESTABLISHED_AS_UNIQUE'

def test_xcop_public_reproduction_numerical_parity():
    x=json.loads((ROOT/'results/xcop_hse_public_reproduction_check.json').read_text())
    assert x['status']=='PASS_NUMERICAL_PARITY'
    assert x['scope']=='PUBLIC_REPRODUCTION_NUMERICAL_PARITY_ONLY'
    assert x['policy_identity_preserved'] is True
    assert x['sample_identity_preserved'] is True
    assert x['heldout_identity_preserved'] is True
    assert x['direction_counts_preserved'] is True
    assert x['delta_signs_preserved'] is True
    assert x['public_replay_audit_status']=='PASS'
    assert x['public_replay_internal_byte_identical'] is True
    assert x['within_numerical_tolerance_1e_10'] is True
    assert max(x['max_absolute_differences'].values()) < 1e-10
