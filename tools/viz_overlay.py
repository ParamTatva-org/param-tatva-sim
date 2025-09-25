import os, json, matplotlib.pyplot as plt

def main(ptk_path="ptk.v1.json", layout_path="ptk.layout.json", emission_json="out/ptk_emission_result.json", out="out/ptk_overlay.png"):
    ptk = json.load(open(ptk_path, "r", encoding="utf-8"))
    layout = json.load(open(layout_path, "r", encoding="utf-8"))
    coords = layout["coords"]
    labels = {n["id"]: n["label"] for n in ptk["nodes"]}

    fig, ax = plt.subplots(figsize=(14,10))
    ax.set_aspect('equal'); ax.axis('off')

    # Edges
    for e in ptk["edges"]:
        x1,y1 = coords[e["source"]]; x2,y2 = coords[e["target"]]
        color = "green" if e["polarity"]==1 else "red"
        ax.plot([x1,x2],[y1,y2], color=color, lw=0.6, alpha=0.35)

    # Nodes
    for nid,(x,y) in coords.items():
        ax.plot(x,y,"o", color="white", mec="black", ms=4, zorder=3)
        ax.text(x,y,labels.get(nid,""), fontsize=7, ha="center", va="center", zorder=4)

    # Emission overlay (if present)
    if os.path.exists(emission_json):
        res = json.load(open(emission_json))
        # Fields: thicken support edges
        support = set(eid for f in res.get("fields", []) for eid in f.get("support_edges", []))
        for e in ptk["edges"]:
            if e["id"] in support:
                x1,y1 = coords[e["source"]]; x2,y2 = coords[e["target"]]
                ax.plot([x1,x2],[y1,y2], lw=2.0, alpha=0.4, color="royalblue")
        # Particles: stars on nodes
        for p in res.get("particles", []):
            x,y = coords[p["locus"]]
            ax.plot(x,y, marker="*", ms=14, mec="black", mfc="gold", zorder=5)

    plt.title("Param Tatva — Positive (green), Negative (red), Fields (blue), Particles (gold)")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    plt.savefig(out, dpi=150)
    print("Wrote", out)

if __name__ == "__main__":
    main()
