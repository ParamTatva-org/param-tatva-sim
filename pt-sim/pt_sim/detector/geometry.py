# pt-sim/pt_sim/detector/geometry.py
from __future__ import annotations
from dataclasses import dataclass
from typing import Tuple, Dict, Any, Optional, List
import json, yaml

@dataclass
class ADC:
    pedestal: float = 200.0
    gain: float = 1.0
    noise_sigma: float = 2.0
    threshold: float = 205.0

@dataclass
class Layer:
    name: str
    type: str
    adc: ADC

@dataclass
class Geometry:
    name: str
    cells_x: int
    cells_y: int
    cell_size_mm: float
    origin_mm: Tuple[float, float]
    layers: List[Layer]

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "Geometry":
        layers = []
        for ld in d.get("layers", []):
            adc = ld.get("adc", {})
            layers.append(Layer(
                name=ld["name"],
                type=ld.get("type", "unknown"),
                adc=ADC(**{k: adc.get(k, getattr(ADC, k, None)) for k in ("pedestal","gain","noise_sigma","threshold")})
            ))
        return cls(
            name=d["name"],
            cells_x=int(d["cells_x"]),
            cells_y=int(d["cells_y"]),
            cell_size_mm=float(d["cell_size_mm"]),
            origin_mm=tuple(d.get("origin_mm", (0.0, 0.0))),
            layers=layers,
        )

    @classmethod
    def from_yaml(cls, path: str) -> "Geometry":
        with open(path, "r") as f:
            data = yaml.safe_load(f)
        return cls.from_dict(data)

    def layer(self, name: str) -> Optional[Layer]:
        for L in self.layers:
            if L.name == name:
                return L
        return None

    def node_to_xy(self, node_id: int) -> Tuple[int, int]:
        x = node_id % self.cells_x
        y = (node_id // self.cells_x) % self.cells_y
        return x, y

    def to_json(self) -> str:
        return json.dumps({
            "name": self.name,
            "cells_x": self.cells_x,
            "cells_y": self.cells_y,
            "cell_size_mm": self.cell_size_mm,
            "origin_mm": self.origin_mm,
            "layers": [ {"name":L.name,"type":L.type,"adc":L.adc.__dict__} for L in self.layers ],
        }, indent=2)
