# pt-sim/pt_sim/detector/run_from_kernel.py
from __future__ import annotations
import argparse, os, json
import numpy as np
from pt_sim.detector.geometry import Geometry
from pt_sim.detector.bridge import kernel_to_ecal_image, kernel_to_adc_counts

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--geom", default="detector/geometry.yaml", help="Path to detector geometry YAML (repo-root relative is fine).")
    ap.add_argument("--seed", type=int, default=123)
    ap.add_argument("--out", default="out/detector")
    args = ap.parse_args()

    # 1) geometry
    geom = Geometry.from_yaml(args.geom)

    # 2) get supported_edges from your kernel (replace with real call)
    # placeholder example: a small cross of energy at center node
    supported_edges = [(geom.cells_x//2 + geom.cells_x*(geom.cells_y//2), 10.0)]

    # 3) image + adc
    img = kernel_to_ecal_image(supported_edges, geom, ribbon_width=1, atten=0.7)
    adc = kernel_to_adc_counts(supported_edges, geom, layer_name="ecal")

    os.makedirs(args.out, exist_ok=True)
    np.save(os.path.join(args.out, "ecal_energy.npy"), img)
    np.save(os.path.join(args.out, "ecal_adc.npy"), adc)
    with open(os.path.join(args.out, "geom.json"), "w") as f:
        f.write(geom.to_json())

if __name__ == "__main__":
    main()
