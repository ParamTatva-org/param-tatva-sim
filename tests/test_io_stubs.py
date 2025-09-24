import numpy as np, os
from pt_sim.io.rootio import write_event_npz, available
from pt_sim.io.hepmc import write_ascii_minimal

def test_npz_writer(tmp_path):
    out = tmp_path / "event.npz"
    p = np.array([[1,2,3]])
    path = write_event_npz(out, {"p": p})
    assert os.path.exists(path)

def test_hepmc_ascii(tmp_path):
    out = tmp_path / "event.hepmc.txt"
    parts = [{"id": 11, "px":0.1, "py":0.2, "pz":1.0, "E":1.05, "status":1}]
    path = write_ascii_minimal(out, parts)
    assert os.path.exists(path)

def test_available_returns_dict():
    info = available()
    assert "root" in info and "backend" in info
