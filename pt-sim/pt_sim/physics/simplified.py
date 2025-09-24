import numpy as np



def lateral_template(n, sigma_cm, cell_size_cm):
    idx = np.arange(n) - (n - 1) / 2
    X, Y = np.meshgrid(idx, idx, indexing="xy")
    X = X * cell_size_cm
    Y = Y * cell_size_cm
    G = np.exp(-0.5 * (X**2 + Y**2) / (sigma_cm**2))
    return G / G.sum()


def longitudinal_profile(depth, alpha, beta, E):
    """
    Toy EM longitudinal profile (gamma-like).
    depth: array in radiation-length units
    alpha,beta: shape/scale-like toy params
    Returns per-layer energy allocating exactly sum(...) == E.
    """
    t = np.asarray(depth, float)
    # Positive, normalized weights
    f = np.power(np.maximum(t, 1e-12), alpha - 1.0) * np.exp(-beta * t)
    wsum = float(f.sum())
    if wsum <= 0.0:
        # fallback to uniform if bad params
        return np.ones_like(t) * (E / max(t.size, 1))
    return E * (f / wsum)

 
