#!/usr/bin/env python
import os, json, math, argparse
from pt_sim.ptk_kernel import PTKKernel, Sound, EmissionConfig

def load_sounds(slist):
    out = []
    for s in slist:
        out.append(Sound(
            node_id=s["node_id"], polarity=int(s["polarity"]),
            energy=float(s["energy"]), frequency=float(s["frequency"]),
            phase=float(s.get("phase", 0.0)), coherence=float(s.get("coherence", 1.0)),
            label=s.get("label","")
        ))
    return out

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--kernel", default="ptk.v1.json", help="Path to ptk.v1.json")
    ap.add_argument("--positive", required=True, help="JSON list of + sounds")
    ap.add_argument("--negative", required=True, help="JSON list of - sounds")
    ap.add_argument("--cfg", default="{}", help="EmissionConfig JSON")
    ap.add_argument("--out", default="out/ptk_emission_result.json")
    args = ap.parse_args()

    ptk = json.load(open(args.kernel, "r", encoding="utf-8"))
    K = PTKKernel(ptk)
    pos = load_sounds(json.loads(args.positive))
    neg = load_sounds(json.loads(args.negative))
    cfg = EmissionConfig(**json.loads(args.cfg))

    res = K.simulate_emission(pos, neg, cfg)
    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    json.dump(res, open(args.out, "w"), indent=2)
    print("Wrote", args.out)

if __name__ == "__main__":
    main()
