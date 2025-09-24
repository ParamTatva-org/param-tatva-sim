"""
Fast-path wrappers. Prefer Rust (pt_core_py) if available, else Python fallback.
"""

try:
    import pt_core_py as _rc  # type: ignore[import-not-found]
    HAVE_RUST = True
except Exception:
    _rc = None
    HAVE_RUST = False


def kk_winding_mass2(m1, m2, w1, w2, r1, r2, alpha_prime):
    if HAVE_RUST:
        return float(
            _rc.kk_winding_mass2_py(
                int(m1),
                int(m2),
                int(w1),
                int(w2),
                float(r1),
                float(r2),
                float(alpha_prime),
            )
        )
    # Python fallback
    return (
        (m1 / r1) ** 2
        + (m2 / r2) ** 2
        + (w1 * r1 / alpha_prime) ** 2
        + (w2 * r2 / alpha_prime) ** 2
    )
