import json, math, os
from pt_sim.ptk_kernel import PTKKernel, Sound, EmissionConfig
from pt_sim.detector.bridge import kernel_to_ecal_image

def test_kernel_to_detector_roundtrip(tmp_path):
    # Load kernel
    ptk = json.load(open("ptk.v1.json", "r", encoding="utf-8"))
    K = PTKKernel(ptk)
    # Emit
    pos = [Sound("n1", +1, 5.0, 440.0, 0.0, 0.9, "P1")]
    neg = [Sound("n4", -1, 5.0, 440.0, 3.14159, 0.9, "N1")]
    res = K.simulate_emission(pos, neg, EmissionConfig(max_steps=30))
    assert "particles" in res and "fields" in res and "detections" in res
    # Detect (image must be non-zero)
    img = kernel_to_ecal_image(res, n=32, e_scale=1.0)
    assert img.shape == (32,32)
    assert float(img.sum()) > 0.0
