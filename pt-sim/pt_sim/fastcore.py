
"""Thin wrapper that prefers Rust-accelerated functions when available.

Build the Python extension from pt-core with:
  cd pt-core
  cargo build --release --features python

Then expose the built library to Python as `pt_core_py` (adjust PYTHONPATH/LD_LIBRARY_PATH
or copy the built .so/.pyd next to this file).
"""
import math
try:
    import pt_core_py as _rc
    HAVE_RUST = True
except Exception:
    _rc = None
    HAVE_RUST = False

def kk_winding_mass2(m1,m2,w1,w2,r1,r2,alpha_prime):
    if HAVE_RUST:
        return float(_rc.kk_winding_mass2_py(int(m1),int(m2),int(w1),int(w2), float(r1),float(r2),float(alpha_prime)))
    # Python fallback
    return (m1/r1)**2 + (m2/r2)**2 + (w1*r1/alpha_prime)**2 + (w2*r2/alpha_prime)**2
