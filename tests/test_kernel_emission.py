import json, math
from pt_sim.ptk_kernel import PTKKernel, Sound, EmissionConfig

def test_emission_produces_outputs():
    ptk = json.load(open("ptk.v1.json"))
    K = PTKKernel(ptk)
    pos = [Sound("n1", +1, 5.0, 440.0, 0.0, 0.9)]
    neg = [Sound("n4", -1, 5.0, 440.0, math.pi, 0.9)]
    res = K.simulate_emission(pos, neg, EmissionConfig(max_steps=20))
    assert ("particles" in res) and ("fields" in res)
    # At least *something* happens in this configuration
    assert (len(res["particles"]) + len(res["fields"])) >= 1
