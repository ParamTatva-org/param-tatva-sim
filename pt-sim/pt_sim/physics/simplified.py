import numpy as np


def lateral_template(n, sigma_cm, cell_size_cm):
    idx = np.arange(n) - (n - 1) / 2
    X, Y = np.meshgrid(idx, idx, indexing="xy")
    X = X * cell_size_cm
    Y = Y * cell_size_cm
    G = np.exp(-0.5 * (X**2 + Y**2) / (sigma_cm**2))
    return G / G.sum()
