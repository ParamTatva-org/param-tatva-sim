from __future__ import annotations
import numpy as np
from typing import Tuple

def adc_response(energy_map: np.ndarray, pedestal=200.0, gain=1.0, noise_sigma=2.0, threshold=205.0) -> np.ndarray:
    """Simple ADC model: pedestal + gain*E + Gaussian noise, with thresholding."""
    noisy = pedestal + gain * energy_map + np.random.normal(0.0, noise_sigma, size=energy_map.shape)
    return np.where(noisy >= threshold, noisy, 0.0)
