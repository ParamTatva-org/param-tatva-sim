import numpy as np

def helix_radius(v_perp, q_over_m, B_mag):
    """r = v_perp / omega,  omega = |q|B/m = |q_over_m|*B."""
    omega = abs(q_over_m) * abs(B_mag)
    return abs(v_perp) / max(omega, 1e-16)

def cyclotron_frequency(q_over_m, B_mag):
    return q_over_m * B_mag
