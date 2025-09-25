# ruff: noqa: E501
# ruff: noqa: E701
"""
PTK Kernel — mypy clean
- Uses a typed Packet dataclass (no ambiguous List[List[...]] indexing)
- Fixes types for by_edge buckets and next_edges keys
- Keeps energy ledger & conservation checks (from earlier patch)
"""

from __future__ import annotations
from dataclasses import dataclass, asdict
from typing import List, Dict, Tuple, Optional, Any
import uuid
import math
import random

# -------------------- Data Models --------------------


@dataclass
class Sound:
    node_id: str
    polarity: int                # +1 or -1
    energy: float
    frequency: float             # Hz (relative)
    phase: float                 # radians
    coherence: float = 1.0       # 0..1
    label: str = ""


@dataclass
class EmissionConfig:
    step_len: float = 1.0
    max_steps: int = 50
    split_decay: float = 0.9
    cancel_bandwidth: float = 0.05
    cancel_phase_tol: float = 0.6
    cancel_efficiency: float = 0.7
    particle_E_thresh: float = 2.0
    field_E_thresh: float = 1.0
    coherence_thresh: float = 0.5
    max_outputs: int = 64
    rng_seed: Optional[int] = 42
    within_gain: float = 1.0
    cross_gain: float = 0.9
    special_gain: float = 1.2
    conservation_tol: float = 1e-6  # relative allowed drift per step


@dataclass
class Particle:
    id: str
    locus: str
    energy: float
    mass2: float
    Q: Dict[str, float]


@dataclass
class Field:
    id: str
    support_edges: List[str]
    energy: float
    strength: float
    mode: str


@dataclass
class DetectionEvent:
    id: str
    kind: str
    ref_id: str
    confidence: float

# Typed packet instead of List[List[float]]


@dataclass
class Packet:
    edge_id: str
    prog: float
    energy: float
    frequency: float
    phase: float
    coherence: float
    polarity: int

# -------------------- Kernel --------------------


class PTKKernel:
    def __init__(self, ptk: Dict[str, Any]):
        self.ptk = ptk
        self.nodes: Dict[str, Dict[str, Any]] = {
            n["id"]: n for n in ptk["nodes"]}
        self.edges: List[Dict[str, Any]] = list(ptk["edges"])
        self.edge_index: Dict[str, Dict[str, Any]] = {
            e["id"]: e for e in self.edges}
        # adjacency by (node, polarity)
        self.next_edges: Dict[Tuple[str, int], List[Dict[str, Any]]] = {}
        for e in self.edges:
            key: Tuple[str, int] = (str(e["source"]), int(e["polarity"]))
            self.next_edges.setdefault(key, []).append(e)

    def _edge_gain(self, e: Dict[str, Any]) -> float:
        t = e["type"]
        w = float(e["flow"].get("weight", 1.0))
        if t == "within_line":
            return self.cfg.within_gain * w
        if t == "cross_sutra":
            return self.cfg.cross_gain * w
        if t == "special":
            return self.cfg.special_gain * w
        return 1.0 * w

    def _charges_from_node(self, node_id: str) -> Dict[str, float]:
        n = self.nodes[node_id]
        return {"line": float(n["line"]), "pos": float(n["pos"])}

    def _init_rng(self, cfg: EmissionConfig) -> None:
        if cfg.rng_seed is not None:
            random.seed(cfg.rng_seed)

    def simulate_emission(self, positive: List[Sound], negative: List[Sound], cfg: Optional[EmissionConfig] = None) -> Dict[str, Any]:
        self.cfg = cfg or EmissionConfig()
        self._init_rng(self.cfg)

        ledger: Dict[str, Any] = {
            "input_energy": 0.0, "steps": [], "final": {}}
        ledger["input_energy"] = sum(s.energy for s in positive + negative)

        # Packets as typed objects
        packets: List[Packet] = []

        def seed(sounds: List[Sound]) -> None:
            for s in sounds:
                outs = self.next_edges.get((s.node_id, s.polarity), [])
                if not outs:
                    continue
                share = s.energy / len(outs)
                for e in outs:
                    packets.append(Packet(
                        edge_id=str(e["id"]), prog=0.0, energy=share,
                        frequency=s.frequency, phase=s.phase,
                        coherence=s.coherence, polarity=s.polarity
                    ))

        seed(positive)
        seed(negative)

        particles: List[Particle] = []
        fields: List[Field] = []
        dets: List[DetectionEvent] = []

        def emit_particle(node_id: str, E: float, coh: float) -> None:
            p = Particle(
                id=str(uuid.uuid4()), locus=node_id, energy=E,
                mass2=E * (0.8 + 0.4 * coh), Q=self._charges_from_node(node_id)
            )
            particles.append(p)
            dets.append(DetectionEvent(
                id=str(uuid.uuid4()), kind="particle", ref_id=p.id,
                confidence=min(1.0, 0.6 + 0.4 * coh)
            ))

        def emit_field(edge_ids: List[str], E: float, coh: float) -> None:
            f = Field(
                id=str(uuid.uuid4()), support_edges=edge_ids[:32], energy=E,
                strength=E * (0.5 + 0.5 * coh), mode=("vector" if coh > 0.7 else "scalar")
            )
            fields.append(f)
            dets.append(DetectionEvent(
                id=str(uuid.uuid4()), kind="field", ref_id=f.id,
                confidence=min(1.0, 0.5 + 0.5 * coh)
            ))

        step = 0
        while step < self.cfg.max_steps and packets and (len(particles) + len(fields) < self.cfg.max_outputs):
            step += 1

            # Bucket packets by edge (typed)
            by_edge: Dict[str, List[Packet]] = {}
            energy_before = sum(p.energy for p in packets)

            for pk in packets:
                e = self.edge_index[pk.edge_id]
                pk.prog += self.cfg.step_len
                pk.energy *= self._edge_gain(e)
                by_edge.setdefault(pk.edge_id, []).append(pk)

            new_packets: List[Packet] = []
            cancelled_energy = 0.0
            field_energy = 0.0
            localized_energy = 0.0

            for edge_id, plist in by_edge.items():
                P = [p for p in plist if p.polarity == +1]
                N = [p for p in plist if p.polarity == -1]

                if P and N:
                    P.sort(key=lambda x: x.frequency)
                    N.sort(key=lambda x: x.frequency)
                    i = j = 0
                    while i < len(P) and j < len(N):
                        p, n = P[i], N[j]
                        df = abs(p.frequency - n.frequency) / \
                            max(1e-6, (p.frequency + n.frequency) / 2.0)
                        dphi = abs(((p.phase - n.phase + math.pi) %
                                   (2 * math.pi)) - math.pi)
                        if df <= self.cfg.cancel_bandwidth and dphi >= (math.pi - self.cfg.cancel_phase_tol):
                            k = self.cfg.cancel_efficiency * \
                                min(p.coherence, n.coherence)
                            dE = k * min(p.energy, n.energy)
                            p.energy -= dE
                            n.energy -= dE
                            cancelled_energy += dE * 2.0
                            field_energy += dE * 0.5
                        if p.frequency <= n.frequency:
                            i += 1
                        else:
                            j += 1

                    if field_energy >= self.cfg.field_E_thresh:
                        coh_vals = [p.coherence for p in P + N]
                        coh_mean = sum(coh_vals) / float(len(coh_vals))
                        emit_field([edge_id], field_energy, coh_mean)

                # Propagate / localize
                e = self.edge_index[edge_id]
                target_node = str(e["target"])
                for pk in plist:
                    if pk.energy <= 1e-12:
                        continue
                    if pk.prog < 1.0:
                        new_packets.append(pk)
                    else:
                        outs = self.next_edges.get(
                            (target_node, pk.polarity), [])
                        if not outs:
                            localized_energy += pk.energy
                            if pk.energy >= self.cfg.particle_E_thresh and pk.coherence >= self.cfg.coherence_thresh:
                                emit_particle(
                                    target_node, pk.energy, pk.coherence)
                        else:
                            share = (pk.energy * self.cfg.split_decay) / \
                                float(len(outs))
                            for oe in outs:
                                new_packets.append(Packet(
                                    edge_id=str(oe["id"]), prog=0.0, energy=share,
                                    frequency=pk.frequency, phase=pk.phase,
                                    coherence=pk.coherence, polarity=pk.polarity
                                ))

            packets = new_packets
            energy_after = sum(p.energy for p in packets)

            removed = max(0.0, energy_before - energy_after)
            accounted = localized_energy + \
                field_energy + (cancelled_energy * 0.5)
            drift = max(0.0, removed - accounted)
            step_rec = {
                "step": step,
                "drift_rel": drift / max(1e-12, energy_before)
            }
            if step_rec["drift_rel"] > self.cfg.conservation_tol:
                step_rec["conservation_warning"] = True
            ledger["steps"].append(step_rec)

        ledger["final"] = {
            "particles_energy": sum(p.energy for p in particles),
            "fields_energy": sum(f.energy for f in fields),
            "remaining_packets_energy": sum(p.energy for p in packets)
        }

        return {
            "particles": [asdict(p) for p in particles],
            "fields": [asdict(f) for f in fields],
            "detections": [asdict(d) for d in dets],
            "steps": step,
            "ledger": ledger
        }


if __name__ == "__main__":
    # Optional demo only; not executed during import
    import json
    demo = json.load(open("ptk.v1.json", "r", encoding="utf-8"))
    K = PTKKernel(demo)
    pos = [Sound("n1", +1, 5.0, 440.0, 0.0, 0.9)]
    neg = [Sound("n4", -1, 5.0, 440.0, math.pi, 0.9)]
    res = K.simulate_emission(pos, neg, EmissionConfig(max_steps=10))
    json.dump(res, open("out/ptk_emission_result_demo.json", "w"), indent=2)
    print("Demo wrote out/ptk_emission_result_demo.json")
