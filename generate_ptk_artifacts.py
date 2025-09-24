# generate_ptk_artifacts.py
# Creates:
#   - ptk.v1.json
#   - ptk.layout.json
#   - ptk_pydantic_validator.py
#   - ptk_rust.rs
#   - ptk_rust_tests.rs

import json, datetime, os, textwrap

# --- 1) Canonical nodes (Maheshwara Sutras, order preserved) ---
LINES = {
    1:  ["a","i","u","Ṇ"],
    2:  ["ṛ","ḷ","K"],
    3:  ["e","o","Ṅ"],
    4:  ["ai","au","C"],
    5:  ["ha","ya","va","ra","Ṭ"],
    6:  ["la","Ṇ"],
    7:  ["ña","ma","ṅa","ṇa","na","M"],
    8:  ["jha","bha","Ñ"],
    9:  ["gha","ḍha","dha","Ṣ"],
    10: ["ja","ba","ga","ḍa","da","Ś"],
    11: ["kha","pha","cha","ṭha","tha","ca","ṭa","ta","V"],
    12: ["ka","pa","Y"],
    13: ["śa","ṣa","sa","R"],
    14: ["ha","L"],
}

DEV_MAP = {
    "a":"अ","i":"इ","u":"उ","Ṇ":"ण्",
    "ṛ":"ऋ","ḷ":"ऌ","K":"क्",
    "e":"ए","o":"ओ","Ṅ":"ङ्",
    "ai":"ऐ","au":"औ","C":"च्",
    "ha":"ह","ya":"य","va":"व","ra":"र","Ṭ":"ट्",
    "la":"ल","ña":"ञ","ma":"म","ṅa":"ङ","ṇa":"ण","na":"न","M":"म्",
    "jha":"झ","bha":"भ","Ñ":"ञ्",
    "gha":"घ","ḍha":"ढ","dha":"ध","Ṣ":"ष्",
    "ja":"ज","ba":"ब","ga":"ग","ḍa":"ड","da":"द","Ś":"श्",
    "kha":"ख","pha":"फ","cha":"छ","ṭha":"ठ","tha":"थ","ca":"च","ṭa":"ट","ta":"त","V":"व्",
    "ka":"क","pa":"प","Y":"य्",
    "śa":"श","ṣa":"ष","sa":"स","R":"र्",
    "L":"ळ"
}

def build_nodes():
    nodes = []
    nid = 1
    for line, arr in LINES.items():
        for pos, lab in enumerate(arr, start=1):
            nodes.append({
                "id": f"n{nid}",
                "label": lab,
                "sanskrit": DEV_MAP.get(lab),
                "line": line,
                "pos": pos,
                "features": []
            })
            nid += 1
    return nodes

# --- 2) Edges: within-line ±, cross-sutra ±, special ha↔ha ± ---
CROSS = [
    ("n4","n24"),("n7","n49"),("n10","n23"),("n13","n45"),
    ("n18","n46"),("n20","n24"),("n26","n22"),("n29","n21"),
    ("n33","n53"),("n39","n52"),("n48","n16"),("n51","n15"),
    ("n55","n17"),("n57","n19"),
]
SPECIAL = ("n14","n56")

def build_edges(nodes):
    # group by line keeping order
    by_line = {}
    for n in nodes:
        by_line.setdefault(n["line"], []).append(n)
    for k in by_line:
        by_line[k].sort(key=lambda x: x["pos"])

    edges = []
    eid = 1

    def add(src, dst, typ, pol, dash, speed, weight):
        nonlocal eid
        edges.append({
            "id": f"e{eid}",
            "source": src, "target": dst,
            "type": typ, "polarity": pol,
            "flow": {"dash": list(dash), "speed": float(speed), "weight": float(weight)}
        })
        eid += 1

    # within-line: positive L→R and negative R→L
    for line, arr in sorted(by_line.items()):
        for i in range(len(arr)-1):
            add(arr[i]["id"], arr[i+1]["id"], "within_line", +1, (6,6), 1.0, 1.8)
        for i in range(len(arr)-1, 0, -1):
            add(arr[i]["id"], arr[i-1]["id"], "within_line", -1, (6,6), 1.0, 1.8)

    # cross-sutra: both polarities
    for s,t in CROSS:
        add(s,t,"cross_sutra", +1, (2,8), 1.3, 1.5)
        add(t,s,"cross_sutra", -1, (2,8), 1.3, 1.5)

    # special ha↔ha: both polarities, thicker
    add(SPECIAL[0], SPECIAL[1], "special", +1, (10,6), 1.6, 3.0)
    add(SPECIAL[1], SPECIAL[0], "special", -1, (10,6), 1.6, 3.0)

    return edges, by_line

# --- 3) Layout (pixel-perfect) ---
CANVAS = {"width": 1800, "height": 1400, "node_w": 70, "node_h": 34}
MARGIN_X, MARGIN_Y, ROW_GAP, COL_GAP = 40, 40, 85, 110

def build_layout(by_line):
    coords = {}
    for line, arr in sorted(by_line.items()):
        total_w = len(arr)*CANVAS["node_w"] + (len(arr)-1)*COL_GAP
        start_x = (CANVAS["width"] - total_w)//2
        y = MARGIN_Y + (line-1)*ROW_GAP
        for i, node in enumerate(arr):
            x = start_x + i*(CANVAS["node_w"] + COL_GAP)
            coords[node["id"]] = [x, y]
    return {"canvas": CANVAS, "coords": coords}

# --- 4) PTK JSON ---
def write_ptk(nodes, edges, by_line, path="ptk.v1.json"):
    ptk = {
        "ptk_version": "1.0",
        "universe": "maheshwara-sutras",
        "meta": {
            "encoding": "unicode",
            "transliteration": "IAST",
            "created": datetime.date.today().isoformat()
        },
        "nodes": nodes,
        "edges": edges,
        "groups": [
            {"name":"line","key": line, "node_ids":[n["id"] for n in arr]}
            for line, arr in sorted(by_line.items())
        ],
        "render_hints": {
            "layout": "rows_by_line",
            "edge_styles": {
                "within_line": {"dash":[6,6]},
                "cross_sutra": {"dash":[2,8]},
                "special": {"dash":[10,6], "weight": 3}
            }
        }
    }
    with open(path, "w", encoding="utf-8") as f:
        json.dump(ptk, f, ensure_ascii=False, indent=2)

# --- 5) Layout JSON ---
def write_layout(layout, path="ptk.layout.json"):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(layout, f, ensure_ascii=False, indent=2)

# --- 6) Python validator (Pydantic) ---
PYD = r'''
from __future__ import annotations
from typing import List, Literal, Optional
from pydantic import BaseModel, Field, validator
import json, sys, hashlib

EdgeType = Literal["within_line", "cross_sutra", "special"]

class Flow(BaseModel):
    dash: List[int] = Field(..., min_items=2, max_items=2)
    speed: float = 1.0
    weight: float = 1.0

class Node(BaseModel):
    id: str
    label: str
    sanskrit: Optional[str] = None
    line: int
    pos: int
    features: List[str] = []

class Edge(BaseModel):
    id: str
    source: str
    target: str
    type: EdgeType
    polarity: int = Field(..., description="+1 or -1")
    flow: Flow

    @validator("polarity")
    def pol_ok(cls, v):
        if v not in (-1, 1):
            raise ValueError("polarity must be +1 or -1")
        return v

class Group(BaseModel):
    name: str
    key: str | int
    node_ids: List[str]

class PTK(BaseModel):
    ptk_version: str
    universe: str
    meta: dict
    nodes: List[Node]
    edges: List[Edge]
    groups: List[Group] = []
    render_hints: dict = {}

    @validator("nodes")
    def unique_node_ids(cls, nodes):
        ids = [n.id for n in nodes]
        if len(ids) != len(set(ids)):
            raise ValueError("duplicate node ids")
        return nodes

    @validator("edges")
    def edge_refs_exist(cls, edges, values):
        node_ids = {n.id for n in values.get("nodes", [])}
        for e in edges:
            if e.source not in node_ids or e.target not in node_ids:
                raise ValueError(f"edge {e.id} has missing node ref")
        return edges

    @validator("edges")
    def polarity_pairs(cls, edges):
        cross = {}
        for e in edges:
            if e.type in ("cross_sutra","special"):
                key = tuple(sorted((e.source, e.target))) + (e.type,)
                cross.setdefault(key, set()).add(e.polarity)
        for k, pols in cross.items():
            if pols != {-1, +1}:
                raise ValueError(f"edge pair missing opposite polarity for {k}")
        return edges

def sha_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path,'rb') as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python ptk_pydantic_validator.py ptk.v1.json")
        sys.exit(2)
    path = sys.argv[1]
    data = json.load(open(path, "r", encoding="utf-8"))
    PTK(**data)  # will raise on invalid
    print("PTK OK:", path)
    print("sha256:", sha_file(path))
'''
def write_pyd(path="ptk_pydantic_validator.py"):
    with open(path, "w", encoding="utf-8") as f:
        f.write(PYD.strip() + "\n")

# --- 7) Rust serde structs ---
RS_STRUCTS = r'''
use serde::{Deserialize, Serialize};

#[derive(Debug, Serialize, Deserialize)]
pub struct Flow {
    pub dash: (u32, u32),
    pub speed: f64,
    pub weight: f64,
}

#[derive(Debug, Serialize, Deserialize)]
#[serde(rename_all = "snake_case")]
pub enum EdgeType {
    WithinLine,
    CrossSutra,
    Special,
}

#[derive(Debug, Serialize, Deserialize)]
pub struct Node {
    pub id: String,
    pub label: String,
    pub sanskrit: Option<String>,
    pub line: u32,
    pub pos: u32,
    pub features: Vec<String>,
}

#[derive(Debug, Serialize, Deserialize)]
pub struct Edge {
    pub id: String,
    pub source: String,
    pub target: String,
    #[serde(rename = "type")]
    pub edge_type: EdgeType,
    pub polarity: i32,
    pub flow: Flow,
}

#[derive(Debug, Serialize, Deserialize)]
pub struct Group {
    pub name: String,
    pub key: serde_json::Value,
    pub node_ids: Vec<String>,
}

#[derive(Debug, Serialize, Deserialize)]
pub struct PTK {
    pub ptk_version: String,
    pub universe: String,
    pub meta: serde_json::Value,
    pub nodes: Vec<Node>,
    pub edges: Vec<Edge>,
    pub groups: Vec<Group>,
    pub render_hints: serde_json::Value,
}
'''
def write_rs_structs(path="ptk_rust.rs"):
    with open(path, "w", encoding="utf-8") as f:
        f.write(RS_STRUCTS.strip() + "\n")

# --- 8) Rust tests for CI ---
RS_TESTS = r'''
use std::fs;
use serde_json::from_str as from_json;
use std::collections::{HashMap, HashSet};

// Adjust imports to your crate path if needed:
// use crate::*; 
// or if placed in a separate crate:
// use param_tatva_kernel::*;

use super::{PTK, EdgeType};

#[test]
fn validate_ptk_kernel() {
    let data = fs::read_to_string("kernel/ptk.v1.json").expect("read ptk.v1.json");
    let ptk: PTK = from_json(&data).expect("valid PTK");

    // Unique node ids
    let mut seen: HashSet<&str> = HashSet::new();
    for n in &ptk.nodes {
        assert!(seen.insert(&n.id), "duplicate node id {}", n.id);
    }

    // Edge references exist and polarity is ±1
    let node_ids: HashSet<_> = ptk.nodes.iter().map(|n| n.id.as_str()).collect();
    for e in &ptk.edges {
        assert!(node_ids.contains(e.source.as_str()), "missing source {}", e.source);
        assert!(node_ids.contains(e.target.as_str()), "missing target {}", e.target);
        assert!(e.polarity == 1 || e.polarity == -1, "polarity must be ±1");
    }

    // Cross/special edges must exist in both polarities
    #[derive(PartialEq, Eq, Hash)]
    struct Key(String,String,String);
    let mut pairs: HashMap<Key, HashSet<i32>> = HashMap::new();
    for e in &ptk.edges {
        match e.edge_type {
            EdgeType::CrossSutra | EdgeType::Special => {
                let (a,b) = if e.source <= e.target { (e.source.clone(), e.target.clone()) } else { (e.target.clone(), e.source.clone()) };
                let t = match e.edge_type {
                    EdgeType::CrossSutra => "cross_sutra".to_string(),
                    EdgeType::Special => "special".to_string(),
                    _ => unreachable!()
                };
                let key = Key(a,b,t);
                pairs.entry(key).or_default().insert(e.polarity);
            }
            _ => {}
        }
    }
    for (_k, pols) in pairs {
        assert!(pols.contains(&1) && pols.contains(&-1), "missing polarity pair");
    }
}
'''
def write_rs_tests(path="ptk_rust_tests.rs"):
    with open(path, "w", encoding="utf-8") as f:
        f.write(RS_TESTS.strip() + "\n")

if __name__ == "__main__":
    nodes = build_nodes()
    edges, by_line = build_edges(nodes)
    layout = build_layout(by_line)

    write_ptk(nodes, edges, by_line, "ptk.v1.json")
    write_layout(layout, "ptk.layout.json")
    write_pyd("ptk_pydantic_validator.py")
    write_rs_structs("ptk_rust.rs")
    write_rs_tests("ptk_rust_tests.rs")

    print("Generated: ptk.v1.json, ptk.layout.json, ptk_pydantic_validator.py, ptk_rust.rs, ptk_rust_tests.rs")
