#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Render Param Tatva kernel (+ / − flows) to a light, animated SVG.

Usage:
  python tools/ptk_draw_svg.py --ptk ptk.v1.json --layout ptk.layout.json --out out/ptk_plus_minus.svg

If --layout is omitted or file not found, a clean fallback layout is computed from line/pos.
"""

import json
import math
import argparse
import os
from typing import Dict, Tuple
from xml.sax.saxutils import escape as esc


GREEN = "#16a34a"  # positive
RED = "#dc2626"  # negative
INK = "#111827"  # text/outline
PANEL = "#ffffff"
BORDER = "#e5e7eb"
HINT = "#6b7280"


def load_ptk(path: str) -> Dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_layout(path: str) -> Dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def compute_layout(ptk: Dict, width=1800, height=1400) -> Dict:
    # Deterministic, readable layout by line/pos
    margin_y, row_gap = 60, 85
    node_w, node_h = 70, 34
    col_gap = 110
    coords = {}
    by_line: Dict[int, list] = {}
    for n in ptk["nodes"]:
        by_line.setdefault(int(n["line"]), []).append(n)
    for line, arr in sorted(by_line.items()):
        arr.sort(key=lambda x: x["pos"])
        total_w = len(arr)*node_w + (len(arr)-1)*col_gap
        start_x = (width - total_w)//2
        y = margin_y + (line-1)*row_gap + 40
        for i, node in enumerate(arr):
            x = start_x + i*(node_w + col_gap)
            coords[node["id"]] = (x, y)
    return {
        "canvas": {"width": width, "height": height, "node_w": node_w, "node_h": node_h},
        "coords": coords
    }


def svg_header(w, h) -> str:
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">
  <defs>
    <marker id="arrowGreen" viewBox="0 0 10 10" refX="10" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="{GREEN}"/>
    </marker>
    <marker id="arrowRed" viewBox="0 0 10 10" refX="10" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="{RED}"/>
    </marker>
    <style>
      .title {{ font: 700 22px/1.2 system-ui, -apple-system, Segoe UI, Roboto, sans-serif; fill:{INK} }}
      .hint  {{ font: 12px/1.2 system-ui; fill:{HINT} }}
      .node text.a {{ font: 600 12.5px ui-sans-serif; fill:{INK} }}
      .node text.b {{ font: 600 11px ui-sans-serif; fill:{HINT} }}
      .node circle {{ fill:#fff; stroke:{INK}; stroke-width:1.1 }}
      .edgeP {{ stroke:{GREEN}; stroke-width:1.6; fill:none; stroke-dasharray:6 8; animation: flowP 2.4s linear infinite }}
      .edgeN {{ stroke:{RED};   stroke-width:1.6; fill:none; stroke-dasharray:6 8; animation: flowN 2.4s linear infinite }}
      .panel {{ fill:{PANEL}; stroke:{BORDER}; stroke-width:1 }}
      @keyframes flowP {{ from {{ stroke-dashoffset: 0 }} to {{ stroke-dashoffset: -28 }} }}
      @keyframes flowN {{ from {{ stroke-dashoffset: 0 }} to {{ stroke-dashoffset:  28 }} }}
    </style>
  </defs>
  <rect x="0" y="0" width="{w}" height="{h}" fill="#ffffff"/>
'''


def svg_footer() -> str:
    return "</svg>\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ptk", required=True, help="Path to ptk.v1.json")
    ap.add_argument("--layout", default="", help="Optional ptk.layout.json")
    ap.add_argument("--out", required=True, help="Output SVG path")
    ap.add_argument(
        "--title", default="Param Tatva — Positive (green) & Negative (red) flows")
    args = ap.parse_args()

    ptk = load_ptk(args.ptk)
    layout = None
    if args.layout and os.path.exists(args.layout):
        layout = load_layout(args.layout)

    if layout is None:
        layout = compute_layout(ptk)

    W = layout.get("canvas", {}).get("width", 1800)
    H = layout.get("canvas", {}).get("height", 1400)
    coords: Dict[str, Tuple[float, float]] = {
        k: tuple(v) for k, v in layout["coords"].items()}

    # Build quick node label map
    label = {n["id"]: n.get("label", "") for n in ptk["nodes"]}
    dev = {n["id"]: n.get("sanskrit", "") or "" for n in ptk["nodes"]}

    # Render
    out = []
    out.append(svg_header(W, H))

    # Title

    out.append(
        f'<text class="title" x="{W/2:.1f}" y="36" text-anchor="middle">{esc(args.title)}</text>\n')

    # Draw a soft panel per sutra line (optional, comment out if too busy)
    by_line: Dict[int, list] = {}
    for n in ptk["nodes"]:
        by_line.setdefault(int(n["line"]), []).append(n)
    for line, arr in sorted(by_line.items()):
        xs = [coords[n["id"]][0] for n in arr]
        ys = [coords[n["id"]][1] for n in arr]
        if not xs or not ys:
            continue
        pad = 30
        x = min(xs)-pad
        y = min(ys)-24
        w = (max(xs)-min(xs))+pad*2
        h = 64
        out.append(
            f'<rect class="panel" x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="12"/>')

    # Edges first (so nodes draw on top)
    for e in ptk["edges"]:
        s, t = e["source"], e["target"]
        if s not in coords or t not in coords:
            continue
        x1, y1 = coords[s]
        x2, y2 = coords[t]
        pol = int(e["polarity"])
        cls   = "edgeP" if pol == 1 else "edgeN"
        marker= "url(#arrowGreen)" if pol == 1 else "url(#arrowRed)"

        dx, dy = (x2 - x1), (y2 - y1)
        length = math.hypot(dx, dy) or 1.0
        offset = 12 if pol == 1 else -12
        ox, oy = -dy/length * offset, dx/length * offset

        cx1 = x1 + dx*0.35 + ox
        cy1 = y1 + dy*0.35 + oy
        cx2 = x1 + dx*0.65 + ox
        cy2 = y1 + dy*0.65 + oy

        out.append(f'<path class="{cls}" d="M {x1:.1f} {y1:.1f} C {cx1:.1f} {cy1:.1f}, {cx2:.1f} {cy2:.1f}, {x2:.1f} {y2:.1f}" marker-end="{marker}"/>')

    # Nodes on top
    for n in ptk["nodes"]:
        nid = n["id"]
        if nid not in coords:
            continue
        x, y = coords[nid]
        roman = label[nid]
        devan = dev[nid]
        out.append(f'<g class="node" transform="translate({x:.1f},{y:.1f})">')
        out.append('<circle r="15"/>')
        out.append(
            f'<text class="a" text-anchor="middle" dy="-20">{devan}</text>')
        out.append(
            f'<text class="b" text-anchor="middle" dy="-4">{roman}</text>')
        out.append('</g>')

    # Legend
    out.append(f'''
  <g transform="translate(20,{H-26})">
    <rect x="0" y="-18" width="{W-40}" height="36" rx="8" fill="#f9fafb" stroke="{BORDER}"/>
    <line x1="20" y1="0" x2="60" y2="0" class="edgeP" marker-end="url(#arrowGreen)"/>
    <text class="hint" x="70" y="4">Positive (+) flow</text>
    <line x1="220" y1="0" x2="260" y2="0" class="edgeN" marker-end="url(#arrowRed)"/>
    <text class="hint" x="270" y="4">Negative (−) flow</text>
  </g>
''')

    out.append(svg_footer())

    os.makedirs(os.path.dirname(args.out) or ".", exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as f:
        f.write("".join(out))
    print("Wrote", args.out)


if __name__ == "__main__":
    main()
