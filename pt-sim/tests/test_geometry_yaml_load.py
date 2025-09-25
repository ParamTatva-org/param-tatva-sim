# pt-sim/tests/test_geometry_yaml_load.py
import os, pyyaml
from pt_sim.detector.geometry import Geometry

def test_geometry_yaml_load():
    assert os.path.exists("detector/geometry.yaml")
    g = Geometry.from_yaml("detector/geometry.yaml")
    assert g.cells_x > 0 and g.cells_y > 0
    assert g.layer("ecal") is not None
