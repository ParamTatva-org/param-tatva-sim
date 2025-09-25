# pt-sim/tests/test_digitization_pipeline.py
import numpy as np
from pt_sim.detector.geometry import Geometry
from pt_sim.detector.bridge import kernel_to_ecal_image, kernel_to_adc_counts

def test_adc_thresholding():
    g = Geometry.from_yaml("detector/geometry.yaml")
    # Inject a single hot cell
    node = (g.cells_x//2) + g.cells_x*(g.cells_y//2)
    img = kernel_to_ecal_image([(node, 10.0)], geom=g)
    adc = kernel_to_adc_counts([(node, 10.0)], geom=g)
    assert adc.sum() >= img.sum()  # pedestal + gain should lift counts
    assert (adc > 0).sum() >= 1    # thresholding yields at least one non-zero channel
