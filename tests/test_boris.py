import numpy as np
from pt_sim.forces.boris import integrate_motion_boris
from pt_sim.forces.gauge import Particle
from pt_sim.forces.analytic import helix_radius, cyclotron_frequency

def uniform_zero_E(t, x): return np.array([0.0,0.0,0.0])
def uniform_Bz(Bz):
    def f(t, x): return np.array([0.0,0.0,Bz])
    return f

def test_uniformB_speed_conservation():
    p = Particle(q=1.0, m=1.0)
    x0 = (0.0,0.0,0.0); v0 = np.array([0.3, 0.0, 0.0])  # keep sub-relativistic
    dt = 0.01; steps = 500
    xs, vs = integrate_motion_boris(p, uniform_zero_E, uniform_Bz(1.0), x0, v0, dt, steps)
    speeds = np.linalg.norm(vs, axis=1)
    #assert speeds.ptp() < 1e-3  # tiny variation
    assert np.ptp(speeds) < 1e-3 

def test_uniformB_helix_radius():
    p = Particle(q=2.0, m=1.0)
    v0 = np.array([0.2, 0.1, 0.0])
    Bz = 0.7
    q_over_m = p.q/p.m
    r_true = helix_radius(np.linalg.norm(v0[:2]), q_over_m, Bz)
    xs, vs = integrate_motion_boris(p, uniform_zero_E, uniform_Bz(Bz), (0,0,0), v0, dt=0.01, steps=2000)
    # Estimate radius from xy positions
    xy = xs[:, :2]
    rc_est = np.mean(np.linalg.norm(xy - xy.mean(axis=0), axis=1))
    assert abs(rc_est - r_true)/r_true < 0.05
