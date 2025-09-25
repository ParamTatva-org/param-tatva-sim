#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Generate a 16:9 SVG illustrating particle & field generation from ± Param Tatva flows.

Usage:
  python tools/ptk_illustration_16x9.py \
    --ptk ptk.v1.json \
    --layout ptk.layout.json \
    --out out/pt_interaction_16x9.svg \
    --highlight-support-edges out/ptk_emission_result.json   # optional

Notes:
- If --layout is absent or missing, a clean fallback layout is computed by (line, pos).
- Positive edges (polarity=+1) = green; Negative edges (polarity=-1) = red.
- Edges are given a small perpendicular offset so both polarities are visible.
- If --highlight-support-edges is provided, edges present in fields[*].support_edges
  are rendered with a thicker blue overlay for emphasis.
"""

import os, json, math, argparse, statistics
from typing import Dict, Tuple, List, Set
from xml.sax.saxutils import escape as esc

GREEN = "#16a34a"   # positive
RED   = "#dc2626"   # negative
INK   = "#111827"   # text/outline
PANEL = "#ffffff"
BORDER= "#e5e7eb"
HINT  = "#6b7280"
FIELD = "#2563eb"
GOLD  = "#f59e0b"

W, H = 1280, 720  # 16:9 canvas

def load_json(path: str):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def compute_layout(ptk: Dict) -> Dict:
    """Fallback layout by sutra line / pos; centered rows for 16:9."""
    node_w, node_h = 70, 34
    margin_y, row_gap, col_gap = 60, 85, 110
    coords: Dict[str, Tuple[float, float]] = {}

    by_line: Dict[int, List[Dict]] = {}
    for n in ptk["nodes"]:
        by_line.setdefault(int(n["line"]), []).append(n)

    for line, arr in sorted(by_line.items()):
        arr.sort(key=lambda x: x["pos"])
        total_w = len(arr)*node_w + (len(arr)-1)*col_gap
        start_x = (W - total_w) // 2
        y = margin_y + (line-1)*row_gap + 120  # middle band for 16:9
        for i, n in enumerate(arr):
            x = start_x + i*(node_w + col_gap)
            coords[n["id"]] = (float(x), float(y))
    return {"canvas": {"width": W, "height": H}, "coords": coords}

def header() -> str:
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  <defs>
    <marker id="arrowGreen" viewBox="0 0 10 10" refX="10" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse">
      <path d="M0 0 L10 5 L0 10Z" fill="{GREEN}"/>
    </marker>
    <marker id="arrowRed" viewBox="0 0 10 10" refX="10" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse">
      <path d="M0 0 L10 5 L0 10Z" fill="{RED}"/>
    </marker>
    <style>
      .title{{font:700 26px/1.2 system-ui,-apple-system,Segoe UI,Roboto,sans-serif;fill:{INK}}}
      .subtitle{{font:600 14px/1.2 system-ui;fill:{HINT}}}
      .legend{{font:600 13px/1.2 system-ui;fill:{INK}}}
      .panel{{fill:{PANEL};stroke:{BORDER};stroke-width:1}}
      .node text.a{{font:700 12px ui-sans-serif;fill:{INK}}}
      .node text.b{{font:600 11px ui-sans-serif;fill:{HINT}}}
      .node circle{{fill:#fff;stroke:{INK};stroke-width:1.1}}
      .edgeP{{stroke:{GREEN};fill:none;stroke-width:1.8;stroke-dasharray:6 8;animation:flowP 2.4s linear infinite}}
      .edgeN{{stroke:{RED};fill:none;stroke-width:1.8;stroke-dasharray:6 8;animation:flowN 2.4s linear infinite}}
      .field{{stroke:{FIELD};fill:none;stroke-width:2;stroke-dasharray:10 10;opacity:.7;animation:wave 3s linear infinite}}
      .fieldHL{{stroke:{FIELD};fill:none;stroke-width:4.2;opacity:.6}}
      .star{{fill:{GOLD};stroke:#00000080;stroke-width:.6;animation:twinkle 1.8s ease-in-out infinite; transform-box: fill-box; transform-origin: center}}
      @keyframes flowP{{from{{stroke-dashoffset:0}}to{{stroke-dashoffset:-28}}}}
      @keyframes flowN{{from{{stroke-dashoffset:0}}to{{stroke-dashoffset: 28}}}}
      @keyframes wave {{from{{stroke-dashoffset:0}}to{{stroke-dashoffset:-80}}}}
      @keyframes twinkle{{0%,100%{{opacity:.9;transform:scale(1)}}50%{{opacity:1;transform:scale(1.15)}}}}
    </style>
  </defs>
  <rect x="0" y="0" width="{W}" height="{H}" fill="#ffffff"/>
'''

def footer() -> str:
    return "</svg>\n"

def bezier_with_offset(x1,y1,x2,y2,polarity,curv=0.35,offset=12):
    """Control points for a cubic curve with perpendicular offset by polarity."""
    dx, dy = (x2 - x1), (y2 - y1)
    length = math.hypot(dx, dy) or 1.0
    off = float(offset if polarity == 1 else -offset)
    ox, oy = -dy/length * off, dx/length * off
    cx1 = x1 + dx*curv + ox
    cy1 = y1 + dy*curv + oy
    cx2 = x1 + dx*(1-curv) + ox
    cy2 = y1 + dy*(1-curv) + oy
    return cx1, cy1, cx2, cy2

def collect_support_edges(emission_path: str) -> Set[str]:
    """Read emission JSON and collect fields[*].support_edges as a set of edge IDs."""
    try:
        em = load_json(emission_path)
    except Exception:
        return set()
    supports: Set[str] = set()
    for f in em.get("fields", []):
        for eid in f.get("support_edges", []):
            if isinstance(eid, str):
                supports.add(eid)
    return supports

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ptk", required=True, help="Path to ptk.v1.json")
    ap.add_argument("--layout", default="", help="Optional ptk.layout.json")
    ap.add_argument("--out", required=True, help="Output SVG path")
    ap.add_argument("--title", default="Param Tatva: Particle & Field Generation from ± Flows")
    ap.add_argument("--highlight-support-edges", default="", help="Path to emission JSON with fields[*].support_edges")
    args = ap.parse_args()

    ptk = load_json(args.ptk)
    layout = load_json(args.layout) if args.layout and os.path.exists(args.layout) else compute_layout(ptk)

    coords: Dict[str, Tuple[float, float]] = {k: tuple(v) for k, v in layout["coords"].items()}
    label = {n["id"]: n.get("label","") for n in ptk["nodes"]}
    dev   = {n["id"]: n.get("sanskrit","") or "" for n in ptk["nodes"]}

    # Optional highlighting from emission
    support_edge_ids: Set[str] = set()
    if args.highlight_support_edges and os.path.exists(args.highlight_support_edges):
        support_edge_ids = collect_support_edges(args.highlight_support_edges)

    out: List[str] = []
    out.append(header())
    out.append(f'<text class="title" x="{W/2}" y="60" text-anchor="middle">{esc(args.title)}</text>')
    out.append(f'<text class="subtitle" x="{W/2}" y="86" text-anchor="middle">Positive (green) meets Negative (red) → particles (stars) &amp; fields (waves)</text>')

    # Faint row panels
    by_line: Dict[int, List[str]] = {}
    for n in ptk["nodes"]:
        by_line.setdefault(int(n["line"]), []).append(n["id"])
    for line, ids in sorted(by_line.items()):
        xs = [coords[i][0] for i in ids if i in coords]
        ys = [coords[i][1] for i in ids if i in coords]
        if not xs or not ys: continue
        pad = 30
        x = min(xs)-pad; y = min(ys)-26
        w = (max(xs)-min(xs))+pad*2
        h = 68
        out.append(f'<rect class="panel" x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="12"/>')

    # Draw normal edges first
    for e in ptk["edges"]:
        s, t = e["source"], e["target"]
        if s not in coords or t not in coords:
            continue
        x1,y1 = coords[s]; x2,y2 = coords[t]
        pol = int(e["polarity"])
        cls = "edgeP" if pol == 1 else "edgeN"
        marker = "url(#arrowGreen)" if pol == 1 else "url(#arrowRed)"
        cx1, cy1, cx2, cy2 = bezier_with_offset(x1,y1,x2,y2,polarity=pol,curv=0.35,offset=12)
        out.append(f'<path class="{cls}" d="M {x1:.1f} {y1:.1f} C {cx1:.1f} {cy1:.1f}, {cx2:.1f} {cy2:.1f}, {x2:.1f} {y2:.1f}" marker-end="{marker}"/>')

    # Overlay support edges thicker in blue (on top), if any
    if support_edge_ids:
        for e in ptk["edges"]:
            if e["id"] not in support_edge_ids:
                continue
            s, t = e["source"], e["target"]
            if s not in coords or t not in coords:
                continue
            x1,y1 = coords[s]; x2,y2 = coords[t]
            pol = int(e["polarity"])
            cx1, cy1, cx2, cy2 = bezier_with_offset(x1,y1,x2,y2,polarity=pol,curv=0.35,offset=12)
            out.append(f'<path class="fieldHL" d="M {x1:.1f} {y1:.1f} C {cx1:.1f} {cy1:.1f}, {cx2:.1f} {cy2:.1f}, {x2:.1f} {y2:.1f}"/>')

    # Draw nodes on top
    for n in ptk["nodes"]:
        nid = n["id"]
        if nid not in coords:
            continue
        x,y = coords[nid]
        out.append(f'<g class="node" transform="translate({x:.1f},{y:.1f})">')
        out.append(  '<circle r="14"/>')
        out.append(  f'<text class="a" text-anchor="middle" dy="-20">{esc(dev[nid])}</text>')
        out.append(  f'<text class="b" text-anchor="middle" dy="-4">{esc(label[nid])}</text>')
        out.append('</g>')

    # Interaction zone near layout median
    Xs = [xy[0] for xy in coords.values()]
    Ys = [xy[1] for xy in coords.values()]
    cx = statistics.median(Xs) if Xs else W/2
    cy = statistics.median(Ys) if Ys else H/2
    out.append(f'<ellipse cx="{cx:.1f}" cy="{cy:.1f}" rx="230" ry="150" fill="rgba(96,165,250,0.08)"/>')
    out.append(f'<text class="legend" x="{cx:.1f}" y="{cy-150:.1f}" text-anchor="middle">Interaction Zone</text>')

    # Illustrative incoming guides
    out.append(f'<path class="edgeP" d="M {cx-180:.1f} {cy-10:.1f} C {cx-120:.1f} {cy-60:.1f}, {cx-60:.1f} {cy-40:.1f}, {cx-10:.1f} {cy-10:.1f}" marker-end="url(#arrowGreen)"/>')
    out.append(f'<path class="edgeN" d="M {cx+180:.1f} {cy+10:.1f} C {cx+120:.1f} {cy+60:.1f}, {cx+60:.1f} {cy+40:.1f}, {cx+10:.1f} {cy+10:.1f}" marker-end="url(#arrowRed)"/>')

    # Particle stars
    def star_points(cx_, cy_, r=11, rot=0):
        return f"{cx_},{cy_-r} {cx_+0.29*r},{cy_-0.31*r} {cx_+0.95*r},{cy_-0.31*r} {cx_+0.41*r},{cy_+0.12*r} {cx_+0.61*r},{cy_+0.80*r} {cx_},{cy_+0.45*r} {cx_-0.61*r},{cy_+0.80*r} {cx_-0.41*r},{cy_+0.12*r} {cx_-0.95*r},{cy_-0.31*r} {cx_-0.29*r},{cy_-0.31*r}"

    out.append(f'<polygon class="star" points="{star_points(cx-20, cy-10)}"/>')
    out.append(f'<polygon class="star" points="{star_points(cx+24, cy+14)}"/>')

    # Field waves
    out.append(f'<path class="field" d="M {cx-220:.1f} {cy:.1f} C {cx-140:.1f} {cy-70:.1f}, {cx-60:.1f} {cy-70:.1f}, {cx+20:.1f} {cy:.1f}"/>')
    out.append(f'<path class="field" d="M {cx-220:.1f} {cy:.1f} C {cx-140:.1f} {cy+70:.1f}, {cx-60:.1f} {cy+70:.1f}, {cx+20:.1f} {cy:.1f}"/>')
    out.append(f'<path class="field" d="M {cx+220:.1f} {cy:.1f} C {cx+140:.1f} {cy-70:.1f}, {cx+60:.1f} {cy-70:.1f}, {cx-20:.1f} {cy:.1f}"/>')
    out.append(f'<path class="field" d="M {cx+220:.1f} {cy:.1f} C {cx+140:.1f} {cy+70:.1f}, {cx+60:.1f} {cy+70:.1f}, {cx-20:.1f} {cy:.1f}"/>')

    # Legend
    out.append(f'''
  <g transform="translate(80,{H-80})">
    <rect x="0" y="-20" width="{W-160}" height="60" rx="10" fill="#f9fafb" stroke="{BORDER}"/>
    <line x1="20" y1="10" x2="60" y2="10" class="edgeP" marker-end="url(#arrowGreen)"/>
    <text class="legend" x="70" y="15">Positive flow (+)</text>

    <line x1="230" y1="10" x2="270" y2="10" class="edgeN" marker-end="url(#arrowRed)"/>
    <text class="legend" x="280" y="15">Negative flow (−)</text>

    <path class="field" d="M 470 10 C 500 -10, 540 -10, 570 10"/>
    <text class="legend" x="580" y="15">Fields (radiative waves)</text>

    <polygon class="star" transform="translate(820,10)" points="0,-8 2.3,-2.5 7.6,-2.5 3.3,1.0 5,6.5 0,3.6 -5,6.5 -3.3,1.0 -7.6,-2.5 -2.3,-2.5"/>
    <text class="legend" x="840" y="15">Particles (localized)</text>

    {"<text class='subtitle' x='"+str(W-160-120)+"' y='15' text-anchor='end'>Support edges highlighted</text>" if support_edge_ids else "<text class='subtitle' x='"+str(W-160-120)+"' y='15' text-anchor='end'>Edge offsets shown for clarity</text>"}
  </g>
''')

    out.append(footer())

    os.makedirs(os.path.dirname(args.out) or ".", exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as f:
        f.write("".join(out))
    print("Wrote", args.out)
    if support_edge_ids:
        print(f"Highlighted {len(support_edge_ids)} support edge(s) from: {args.highlight_support_edges}")

if __name__ == "__main__":
    main()
