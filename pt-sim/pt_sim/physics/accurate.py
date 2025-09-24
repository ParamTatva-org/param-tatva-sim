import numpy as np


def lateral_em(n, cell_size_cm, RM_cm, core_frac: float = 0.8):
    idx = np.arange(n) - (n - 1) / 2
    X, Y = np.meshgrid(idx, idx, indexing="xy")
    X = X * cell_size_cm
    Y = Y * cell_size_cm
    R2 = X**2 + Y**2
    sc = 0.3 * RM_cm
    st = 1.0 * RM_cm
    Gc = np.exp(-0.5 * R2 / (sc**2))
    Gt = np.exp(-0.5 * R2 / (st**2))
    M = core_frac * Gc + (1.0 - core_frac) * Gt
    return M / M.sum()


def longitudinal_em(depth, E, X0_cm: float, Ec_MeV: float):
    """
    Toy, PDG-inspired gamma-like longitudinal profile with energy closure.
    depth: array in X0 units (already scaled)
    E: GeV
    X0_cm, Ec_MeV are accepted for future realism; not used in the toy shape.
    """
    t = np.asarray(depth, float)
    # Shape parameter grows (weakly) with E/Ec; keep >=1
    a = float(np.log(max(E * 1e3 / max(Ec_MeV, 1e-6), 1.01)) + 1.0)
    b = 1.0
    f = np.power(np.maximum(t, 1e-12), a - 1.0) * np.exp(-b * t)
    wsum = float(f.sum())
    if wsum <= 0.0:
        return np.ones_like(t) * (E / max(t.size, 1))
    return E * (f / wsum)


def digitize_energy(
    ecal_true,
    sampling_fraction,
    light_yield_pe_per_GeV,
    electronics_noise_GeV,
    rng,
):
    mean_signal = sampling_fraction * ecal_true
    mean_pe = mean_signal * light_yield_pe_per_GeV
    # Poisson at low mean, Gaussian approx at high mean
    out = np.empty_like(mean_signal, dtype=float)
    low = mean_pe < 20.0
    high = ~low
    out[low] = rng.poisson(mean_pe[low]).astype(float) / np.maximum(
        light_yield_pe_per_GeV, 1e-12
    )
    out[high] = (
        mean_signal[high]
        + rng.normal(
            0.0,
            np.sqrt(mean_pe[high]) / np.maximum(light_yield_pe_per_GeV, 1e-12),
        )
    )
    out += rng.normal(0.0, electronics_noise_GeV, size=out.shape)
    out = np.clip(out, 0.0, None)
    return out


 
