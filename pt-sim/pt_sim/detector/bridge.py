# pt-sim/pt_sim/detector/bridge.py
from __future__ import annotations
from typing import TYPE_CHECKING, Any, Dict, Iterable, List, Optional, Tuple, Union, cast
import numpy as np

# ---- static types only (for mypy) ----
if TYPE_CHECKING:
    from pt_sim.detector.geometry import Geometry, Layer, ADC
    from pt_sim.detector.digitize import adc_response as AdcResponseFunc

# ---- runtime symbols (assign once, then fill in try-block) ----
_Geometry: Any = None
_Layer: Any = None
_ADC: Any = None
_adc_response: Any = None

try:
    from pt_sim.detector.geometry import Geometry as rtGeometry, Layer as rtLayer, ADC as rtADC
    from pt_sim.detector.digitize import adc_response as rt_adc_response
    _Geometry = rtGeometry
    _Layer = rtLayer
    _ADC = rtADC
    _adc_response = rt_adc_response
except Exception:  # pragma: no cover
    pass



# ---------------- Utilities & compatibility ----------------

def _to_int(x: object) -> int:
    if isinstance(x, (int, np.integer)):  # np.integer allowed
        return int(x)
    raise TypeError(f"Expected int-like for node id, got {type(x).__name__}")

def _have_geometry_runtime() -> bool:
    return _Geometry is not None and _Layer is not None and _ADC is not None

def _ensure_geom(geom: Optional["Geometry"], n: Optional[int]) -> "Geometry":
    if geom is not None:
        return geom
    if _Geometry is None or _Layer is None or _ADC is None:
        raise RuntimeError("Geometry types not available at runtime; cannot synthesize geometry.")
    if not n:
        n = 32
    g = _Geometry.__new__(_Geometry)
    g.name = "auto-n"
    g.cells_x = int(n)
    g.cells_y = int(n)
    g.cell_size_mm = 10.0
    g.origin_mm = (0.0, 0.0)
    g.layers = [_Layer(name="ecal", type="sampling", adc=_ADC())]
    return cast("Geometry", g)


def _qp_to_node(line: int, pos: int, n: int) -> int:
    x = (line - 1) % n
    y = (pos - 1) % n
    return x + y * n

def _extract_supported_edges(result: Dict[str, Any], n: int, scale: float) -> List[Tuple[int, float]]:
    edges: List[Tuple[int, float]] = []

    # Preferred: fields[*].support_edges
    for f in (result.get("fields") or []):
        if isinstance(f, dict):
            se = f.get("support_edges")
            if isinstance(se, list) and se and isinstance(se[0], (list, tuple)):
                for node, e in se:
                    edges.append((_to_int(node), float(e) * scale))

    if edges:
        return edges

    # Fallback: particles/fields with Q & energy
    def add_from_Q(obj: Dict[str, Any]) -> None:
        Q = obj.get("Q") or {}
        line = int(Q.get("line", 1))
        pos = int(Q.get("pos", 1))
        e = float(obj.get("energy", 0.0)) * scale
        if e != 0.0:
            edges.append((_qp_to_node(line, pos, n), e))

    for p in (result.get("particles") or []):
        if isinstance(p, dict):
            add_from_Q(p)
    for f in (result.get("fields") or []):
        if isinstance(f, dict):
            add_from_Q(f)

    if not edges:
        total_e = float(result.get("total_energy", 0.0)) * scale
        if total_e != 0.0:
            center = _qp_to_node((n // 2) + 1, (n // 2) + 1, n)
            edges.append((center, total_e))

    return edges


# ---------------- Core image builders (new API with legacy compat) ----------------

def kernel_to_ecal_image(
    result_or_edges: Union[Dict[str, Any], Iterable[Tuple[int, float]]],
    *args,  # legacy positional: Geometry or int(n)
    geom: Optional["Geometry"] = None,
    n: Optional[int] = None,
    E_scale: Optional[float] = None,
    e_scale: Optional[float] = None,
    ribbon_width: int = 1,
    atten: float = 1.0,
) -> np.ndarray:
    # Compat for positional 2nd arg
    if args:
        a = args[0]
        if _have_geometry_runtime() and hasattr(a, "cells_x") and hasattr(a, "cells_y"):
            geom = a  
        elif isinstance(a, int):
            n = a
        else:
            raise TypeError("Second positional arg must be Geometry or int (n)")

    scale = e_scale if e_scale is not None else (E_scale if E_scale is not None else 1.0)
    G = _ensure_geom(geom, n)

    # Normalize to supported_edges iterable
    if isinstance(result_or_edges, dict):
        N = int(n) if n is not None else int(getattr(G, "cells_x", 32))
        supported_edges = _extract_supported_edges(result_or_edges, N, scale)
    else:
        supported_edges = [(_to_int(i), float(e) * scale) for (i, e) in result_or_edges]

    img = np.zeros((G.cells_y, G.cells_x), dtype=float)
    for node_id, e in supported_edges:
        x = node_id % G.cells_x
        y = (node_id // G.cells_x) % G.cells_y
        x0, x1 = max(0, x - ribbon_width), min(G.cells_x, x + ribbon_width + 1)
        y0, y1 = max(0, y - ribbon_width), min(G.cells_y, y + ribbon_width + 1)
        patch = img[y0:y1, x0:x1]
        ky = np.abs(np.arange(y0, y1) - y)[:, None]
        kx = np.abs(np.arange(x0, x1) - x)[None, :]
        kernel = np.power(atten, ky + kx)
        patch += e * kernel
    return img


def kernel_to_adc_counts(
    result_or_edges: Union[Dict[str, Any], Iterable[Tuple[int, float]]],
    *args,
    geom: Optional["Geometry"] = None,
    n: Optional[int] = None,
    layer_name: str = "ecal",
    E_scale: Optional[float] = None,
    e_scale: Optional[float] = None,
    ribbon_width: int = 1,
    atten: float = 1.0,
) -> np.ndarray:
    if args:
        a = args[0]
        if _Geometry is not None and hasattr(a, "cells_x") and hasattr(a, "cells_y"):
            geom = a  # runtime Geometry
        elif isinstance(a, int):
            n = a
        else:
            raise TypeError("Second positional arg must be Geometry or int (n)")

    scale = e_scale if e_scale is not None else (E_scale if E_scale is not None else 1.0)
    G = _ensure_geom(geom, n)

    img = kernel_to_ecal_image(
        result_or_edges,
        geom=G,
        ribbon_width=ribbon_width,
        atten=atten,
        E_scale=scale,
    )

    # Defaults
    ped, gain, noise, thr = 200.0, 1.0, 2.0, 205.0

    # If geometry exposes a 'layer' method with adc settings, use them
    layer_fn = getattr(G, "layer", None)
    if callable(layer_fn):
        layer = layer_fn(layer_name)  # runtime object
        if layer is None:
            raise ValueError(f"Layer '{layer_name}' not found in geometry.")
        ped = float(layer.adc.pedestal)
        gain = float(layer.adc.gain)
        noise = float(layer.adc.noise_sigma)
        thr = float(layer.adc.threshold)

    if _adc_response is not None:
        return _adc_response(img, pedestal=ped, gain=gain, noise_sigma=noise, threshold=thr)

    noisy = ped + gain * img
    return np.where(noisy >= thr, noisy, 0.0)

