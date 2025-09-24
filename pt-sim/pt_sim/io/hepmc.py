from pathlib import Path

def write_ascii_minimal(path, particles):
    """
    Very small, HepMC-like ASCII for tests. 'particles' is list of dicts with keys:
      id, px, py, pz, E, status
    """
    path = Path(path); path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        f.write("# Minimal HepMC-like ASCII (ParamTatva)\n")
        for p in particles:
            f.write(f"P {p['id']} {p['px']} {p['py']} {p['pz']} {p['E']} {p.get('status',1)}\n")
    return str(path)
