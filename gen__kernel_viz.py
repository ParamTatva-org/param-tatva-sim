import os, json
import matplotlib.pyplot as plt

res_path = "out/ptk_emission_result.json"

res = json.load(open(res_path)) if os.path.exists(res_path) else None


# Load kernel JSON
with open("ptk.v1.json", "r", encoding="utf-8") as f:
    ptk = json.load(f)

coords = {}
# Try to load layout too (pixel-perfect positions)
layout_path = "ptk.layout.json"
try:
    with open(layout_path, "r", encoding="utf-8") as f:
        layout = json.load(f)
    coords = layout["coords"]
except FileNotFoundError:
    # fallback: simple layered layout by line
    node_w, node_h = 70, 34
    row_gap, col_gap = 85, 110
    margin_x, margin_y = 40, 40
    nodes_by_line = {}
    for n in ptk["nodes"]:
        nodes_by_line.setdefault(n["line"], []).append(n)
    for line in nodes_by_line:
        nodes_by_line[line].sort(key=lambda x: x["pos"])
        total_w = len(nodes_by_line[line])*node_w + (len(nodes_by_line[line])-1)*col_gap
        start_x = margin_x
        y = margin_y + (line-1)*row_gap
        for idx, n in enumerate(nodes_by_line[line]):
            x = start_x + idx*(node_w+col_gap)
            coords[n["id"]] = [x,y]

# Build dict for labels
labels = {n["id"]: n["label"] for n in ptk["nodes"]}

# Draw
fig, ax = plt.subplots(figsize=(14, 10))
ax.set_aspect('equal')
ax.axis('off')

# Draw edges
for e in ptk["edges"]:
    src, dst = e["source"], e["target"]
    if src not in coords or dst not in coords:
        continue
    x1,y1 = coords[src]
    x2,y2 = coords[dst]
    color = "green" if e["polarity"]==1 else "red"
    ax.annotate("",
                xy=(x2,y2), xycoords='data',
                xytext=(x1,y1), textcoords='data',
                arrowprops=dict(arrowstyle="->", color=color,
                                lw=0.8, alpha=0.6))

# Draw nodes
for nid,(x,y) in coords.items():
    ax.plot(x,y,"o", color="white", mec="black")
    ax.text(x,y,labels.get(nid,""), fontsize=8,
            ha="center", va="center")


if res:
    # fields: highlight support edges
    field_edge_ids = set(eid for f in res["fields"] for eid in f["support_edges"])
    for e in ptk["edges"]:
        if e["id"] in field_edge_ids:
            x1,y1 = coords[e["source"]]; x2,y2 = coords[e["target"]]
            ax.plot([x1,x2],[y1,y2], lw=2.4, alpha=0.35)  # thicker wash

    # particles: draw star markers at locus nodes
    for p in res["particles"]:
        x,y = coords[p["locus"]]
        ax.plot(x,y, marker="*", ms=12, mec="black", mfc="gold", zorder=5)
        
plt.title("Param Tatva Kernel — Positive (green) & Negative (red) flows")
plt.tight_layout()
outpath = "ptk_overlay_flows.png"
plt.savefig(outpath, dpi=150)
outpath
