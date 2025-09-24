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
