import yaml, numpy as np
from pt_sim.detector.geometry import Geometry

def test_linear_node_to_xy():
    d = {
        "name":"toy",
        "cells_x": 4,
        "cells_y": 4,
        "cell_size_mm": 10.0,
        "origin_mm": [0.0, 0.0],
    }
    g = Geometry.from_dict(d)
    assert g.node_to_xy(0) == (0,0)
    assert g.node_to_xy(3) == (3,0)
    assert g.node_to_xy(4) == (0,1)
