import json, math
from pt_sim.ptk_kernel import PTKKernel, Sound, EmissionConfig

def test_energy_conservation_drift_under_threshold():
    ptk = json.load(open("ptk.v1.json"))
    K = PTKKernel(ptk)
    pos = [Sound("n1", +1, 5.0, 440.0, 0.0, 0.9)]
    neg = [Sound("n4", -1, 5.0, 440.0, math.pi, 0.9)]
    cfg = EmissionConfig(max_steps=20, conservation_tol=1e-4, rng_seed=123)
    res = K.simulate_emission(pos, neg, cfg)
    drifts = [s['drift_rel'] for s in res['ledger']['steps']]
    assert all(d <= cfg.conservation_tol*10 for d in drifts)
