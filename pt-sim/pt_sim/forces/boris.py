import numpy as np
from .gauge import Particle

def boris_step(q_over_m, dt, v, E, B, relativistic=False, c=1.0):
    """
    Single Boris push.
    If relativistic=True, uses gamma from v at the beginning of the step.
    Units: c can be 1.0 (natural units). Keep speeds well below c if non-relativistic.
    """
    v = np.asarray(v, float); E = np.asarray(E, float); B = np.asarray(B, float)
    if relativistic:
        v2 = np.dot(v, v)
        gamma = 1.0 / np.sqrt(max(1.0 - v2/(c*c), 1e-12))
    else:
        gamma = 1.0
    # Half electric kick
    v_minus = v + (q_over_m * E) * (dt * 0.5) / gamma
    # Magnetic rotation
    t = q_over_m * B * (dt * 0.5) / gamma
    t2 = np.dot(t, t)
    v_prime = v_minus + np.cross(v_minus, t)
    s = 2.0 * t / (1.0 + t2)
    v_plus = v_minus + np.cross(v_prime, s)
    # Half electric kick
    v_new = v_plus + (q_over_m * E) * (dt * 0.5) / gamma
    return v_new

def integrate_motion_boris(p: Particle, E_func, B_func, x0, v0, dt, steps, relativistic=False, c=1.0):
    """
    Integrate trajectory with Boris pusher. E_func(t,x)->E, B_func(t,x)->B.
    Returns arrays xs, vs (shape [steps,3]).
    """
    x = np.array(x0, float); v = np.array(v0, float)
    xs = np.zeros((steps, 3)); vs = np.zeros((steps, 3))
    q_over_m = p.q / max(p.m, 1e-12)
    t = 0.0
    for i in range(steps):
        E = np.asarray(E_func(t, x), float)
        B = np.asarray(B_func(t, x), float)
        # Boris velocity update
        v = boris_step(q_over_m, dt, v, E, B, relativistic=relativistic, c=c)
        # Position update (leapfrog consistent)
        x = x + v * dt
        xs[i] = x; vs[i] = v
        t += dt
    return xs, vs
