import numpy as np
from pt_sim.physics import simplified as ps
from pt_sim.physics import accurate as pa

def test_energy_closure_simplified():
    n = 32; E = 5.0
    depth = np.linspace(0, 20.0, n)
    longE = ps.longitudinal_profile(depth, 4.0, 0.3, E)
    lat = ps.lateral_template(n, 1.2, 1.0)
    e = sum(ei*lat for ei in longE)
    assert abs(e.sum()-E)/E < 5e-3

def test_energy_closure_accurate():
    n = 32; E = 5.0
    depth = np.linspace(0, 20.0, n)
    longE = pa.longitudinal_em(depth, E, X0_cm=1.0, Ec_MeV=10.0)
    lat = pa.lateral_em(n, 1.0, RM_cm=2.0)
    e = sum(ei*lat for ei in longE)
    assert abs(e.sum()-E)/E < 5e-3
