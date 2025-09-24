import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import json

# Re-load kernel
with open("ptk.v1.json", "r", encoding="utf-8") as f:
    ptk = json.load(f)

with open("ptk.layout.json", "r", encoding="utf-8") as f:
    layout = json.load(f)

coords = layout["coords"]
labels = {n["id"]: n["label"] for n in ptk["nodes"]}

# Precompute edge lines
edges_pos, edges_neg = [], []
for e in ptk["edges"]:
    src, dst = e["source"], e["target"]
    if src not in coords or dst not in coords: 
        continue
    x1,y1 = coords[src]
    x2,y2 = coords[dst]
    if e["polarity"] == 1:
        edges_pos.append(((x1,y1),(x2,y2)))
    else:
        edges_neg.append(((x1,y1),(x2,y2)))

fig, ax = plt.subplots(figsize=(14,10))
ax.set_aspect('equal')
ax.axis('off')

# Draw nodes
for nid,(x,y) in coords.items():
    ax.plot(x,y,"o", color="white", mec="black", zorder=3)
    ax.text(x,y,labels.get(nid,""), fontsize=7, ha="center", va="center", zorder=4)

# Collections for animated arrows
pos_lines = [ax.plot([],[], color="green", lw=1, alpha=0.6)[0] for _ in edges_pos]
neg_lines = [ax.plot([],[], color="red", lw=1, alpha=0.6)[0] for _ in edges_neg]

def init():
    for ln in pos_lines+neg_lines:
        ln.set_data([],[])
    return pos_lines+neg_lines

def animate(frame):
    # animate along each edge with a moving dot or pulsing segment
    frac = (frame % 30) / 30.0
    for ln,(p1,p2) in zip(pos_lines, edges_pos):
        x1,y1 = p1; x2,y2 = p2
        xm, ym = x1 + frac*(x2-x1), y1 + frac*(y2-y1)
        ln.set_data([x1,xm],[y1,ym])
    for ln,(p1,p2) in zip(neg_lines, edges_neg):
        x1,y1 = p1; x2,y2 = p2
        xm, ym = x1 + frac*(x2-x1), y1 + frac*(y2-y1)
        ln.set_data([x1,xm],[y1,ym])
    return pos_lines+neg_lines

ani = animation.FuncAnimation(fig, animate, init_func=init,
                              frames=60, interval=100, blit=True)

outpath = "ptk_overlay_flows.gif"
ani.save(outpath, writer="pillow", dpi=120)
outpath
