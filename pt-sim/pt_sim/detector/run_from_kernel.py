import json, numpy as np
from .bridge import kernel_to_ecal_image
from ..io.rootio import write_event_npz

def run(emission_json="out/ptk_emission_result.json", out="out/detected_event.npz"):
    res = json.load(open(emission_json))
    img = kernel_to_ecal_image(res, n=32, E_scale=1.0)
    write_event_npz(out, {"ecal": img.astype(np.float32)})
    print("Wrote", out)

if __name__ == "__main__":
    run()
