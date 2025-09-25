import os
import json
import numpy as np
from .bridge import kernel_to_ecal_image

def run(emission_json="out/ptk_emission_result.json", out_npz="out/detected_event.npz", n=32):
    os.makedirs(os.path.dirname(out_npz), exist_ok=True)
    res = json.load(open(emission_json, "r", encoding="utf-8"))
    img = kernel_to_ecal_image(res, n=n, e_scale=1.0)
    np.savez_compressed(out_npz, ecal=img.astype(np.float32))
    print("Wrote", out_npz)

if __name__ == "__main__":
    run()
