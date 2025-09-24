from pathlib import Path
import numpy as np


def write_event_npz(path, arrays: dict):
    """Safe default: writes numpy .npz file so tests pass without ROOT."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(path, **arrays)
    return str(path)


def available():
    """Return a tiny capability struct; extend when ROOT/uproot present."""
    try:
        import uproot  # noqa: F401
        return {"root": True, "backend": "uproot"}
    except Exception:
        return {"root": False, "backend": "npz"}
