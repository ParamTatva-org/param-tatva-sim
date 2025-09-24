import numpy as np, json
from pt_sim.detector.bridge import kernel_to_ecal_image

def test_bridge_image_nonzero(tmp_path):
    dummy = {"particles":[{"Q":{"line":5,"pos":2},"energy":3.0}], "fields":[{"energy":1.5,"support_edges":[]}]}
    img = kernel_to_ecal_image(dummy, n=32, E_scale=1.0)
    assert img.shape == (32,32)
    assert float(img.sum()) > 0.0
