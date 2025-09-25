# ruff: noqa: E501
# ruff: noqa: E701
import numpy as np
from typing import Dict, Any, Tuple


def _node_to_xy(node_line: int, node_pos: int, n: int) -> Tuple[int, int]:
    # Simple deterministic mapping onto a grid: ring-by-line, angle-by-pos
    # Tweak later if you have a real geometry.
    r = int((n*0.15) + (node_line/14.0)*(n*0.35))
    c = int((n*0.15) + (node_pos/9.0)*(n*0.6))
    r = max(0, min(n-1, r))
    c = max(0, min(n-1, c))
    return r, c



def kernel_to_ecal_image(emission: Dict[str, Any], n: int = 32, e_scale: float = 1.0, **kwargs) -> np.ndarray:
    # Back-compat alias
    if "E_scale" in kwargs and kwargs["E_scale"] is not None:
        e_scale = kwargs["E_scale"]
        
    """Convert kernel outputs to a toy ECAL-like 2D image."""
    img = np.zeros((n, n), float)

    # Particles -> localized Gaussian deposits
    for p in emission.get("particles", []):
        line = int(p["Q"].get("line", 1))
        pos = int(p["Q"].get("pos", 1))
        r, c = _node_to_xy(line, pos, n)
        rr, cc = np.meshgrid(np.arange(n), np.arange(n), indexing="ij")
        sigma = max(1.0, 0.6 + 0.04*p["energy"])
        blob = np.exp(-0.5*((rr-r)**2+(cc-c)**2)/(sigma**2))
        img += e_scale * p["energy"] * blob

    # Fields -> diffuse background (proportional to energy and edge count)
    total_field_E = sum(f["energy"] for f in emission.get("fields", []))
    if total_field_E > 0:
        img += e_scale * 0.3 * total_field_E / (n*n)

    return img
