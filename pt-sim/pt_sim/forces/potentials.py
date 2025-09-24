import numpy as np


def coulomb_potential(r, alpha: float = 1.0):
    r = np.maximum(r, 1e-6)
    return alpha / r


def yukawa_potential(r, g: float = 1.0, m: float = 1.0):
    r = np.maximum(r, 1e-6)
    return (g**2) * np.exp(-m * r) / r


def string_potential(r, kappa: float = 1.0, c: float = 0.0):
    return kappa * r + c
