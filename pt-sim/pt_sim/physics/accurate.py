import numpy as np
def _gamma_profile(depth, a, b, E):
  xs = np.linspace(0, depth.max(), 4096)
  ys = (xs**(a-1)) * np.exp(-b*xs)
  norm = np.trapz(ys, xs)
  return (depth**(a-1)) * np.exp(-b*depth) * (E / norm)
def longitudinal_em(depth, E_GeV, X0_cm, Ec_MeV):
  E_MeV = E_GeV * 1e3
  a = 1.0 + 0.5 * np.log(max(E_MeV, 1.0) / max(Ec_MeV, 1.0))
  b = 1.0
  return _gamma_profile(depth, a, b, E_GeV)
def lateral_em(n, cell_size_cm, RM_cm, core_frac=0.8):
  idx = np.arange(n) - (n-1)/2
  X, Y = np.meshgrid(idx, idx, indexing='xy')
  X = X * cell_size_cm; Y = Y * cell_size_cm
  R2 = X**2 + Y**2
  sc = 0.3 * RM_cm; st = 1.0 * RM_cm
  Gc = np.exp(-0.5 * R2 / (sc**2))
  Gt = np.exp(-0.5 * R2 / (st**2))
  M = core_frac * Gc + (1.0 - core_frac) * Gt
  return M / M.sum()
def digitize_energy(ecal_true, sampling_fraction, light_yield_pe_per_GeV, electronics_noise_GeV, rng):
  mean_signal = sampling_fraction * ecal_true
  mean_pe = mean_signal * light_yield_pe_per_GeV
  pe = rng.normal(mean_pe, np.sqrt(np.maximum(mean_pe, 1.0)))
  pe = np.clip(pe, 0.0, None)
  signal = pe / light_yield_pe_per_GeV
  return np.clip(signal + rng.normal(0.0, electronics_noise_GeV, size=ecal_true.shape), 0, None)
