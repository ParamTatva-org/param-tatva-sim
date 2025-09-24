from __future__ import annotations

# Write a robust, reference Python kernel for "sound emission" interactions over PTK.
# It will:
# - Load PTK v1 JSON
# - Define Sound packets with polarity (+1/-1), energy, phase, frequency
# - Propagate packets along edges respecting polarity
# - Handle interactions (partial/total cancellation) of opposite-polarity packets on same edge
# - Emit particles and fields from residual energies (can produce multiple outputs)
# - Return a structured result JSON for study (generation + detection stubs)


import json
import math
import uuid
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional, Any
from typing import Union, Tuple




from collections import defaultdict
from typing import DefaultDict, Dict, List, Tuple, TypeAlias, Any



NodeId: TypeAlias = str          # node ids are "n1", "n4", ...
Polarity: TypeAlias = int         # +1 or -1
EdgeKey: TypeAlias = Tuple[NodeId, Polarity]
Edge:    TypeAlias = Dict[str, Any]


ptk_path = "ptk.v1.json"

# ---------- Data Models ----------

@dataclass
class Sound:
    node_id: str                # start node
    polarity: int               # +1 or -1
    energy: float               # arbitrary units
    frequency: float            # Hz (relative)
    phase: float                # radians
    coherence: float = 1.0      # 0..1 quality factor
    label: str = ""             # optional tag

@dataclass
class EmissionConfig:
    step_len: float = 1.0               # normalized distance per step along an edge
    max_steps: int = 50                 # hard cap on steps
    split_decay: float = 0.9            # loss when splitting at nodes
    line_bias: float = 1.0              # multiplier for within_line edges
    cross_bias: float = 0.85            # multiplier for cross_sutra edges
    special_bias: float = 1.25          # multiplier for special edges
    cancel_bandwidth: float = 0.05      # relative frequency tolerance for cancellation
    cancel_phase_tol: float = 0.6       # radians tolerance for near-antiphase
    cancel_efficiency: float = 0.7      # fraction of matched energies that cancel
    particle_E_thresh: float = 2.0      # minimum localized residual energy to spawn particle
    field_E_thresh: float = 1.0         # minimum delocalized residual energy to spawn field
    coherence_thresh: float = 0.5       # minimum coherence to spawn structured outputs
    max_outputs: int = 64               # safety cap for outputs

@dataclass
class Particle:
    id: str
    locus: str                 # node id
    energy: float
    mass2: float               # toy relation: proportional to energy
    Q: Dict[str, float]        # charges/labels derived from node lineage

@dataclass
class Field:
    id: str
    support_edges: List[str]   # edge ids where the field is distributed
    energy: float
    strength: float            # aggregate measure
    mode: str                  # "vector" | "scalar" (toy)

@dataclass
class DetectionEvent:
    id: str
    kind: str                  # "particle" | "field"
    ref_id: str                # particle.id or field.id
    confidence: float

# ---------- Kernel Implementation ----------

class PTKKernel:
    def __init__(self, ptk: Dict[str, Any]):
        self.ptk = ptk

        self.nodes: Dict[NodeId, Dict[str, Any]] = {n["id"]: n for n in ptk["nodes"]}


        # keyed by (node_id, polarity)
        self.out_edges: DefaultDict[EdgeKey, List[Edge]] = defaultdict(list)
        self.in_edges:  DefaultDict[EdgeKey, List[Edge]] = defaultdict(list)

        # build adjacency
        for e in ptk["edges"]:
            src: NodeId = e["source"]
            tgt: NodeId = e["target"]
            pol: Polarity = int(e["polarity"])
            self.out_edges.setdefault((src, pol), []).append(e)
            self.in_edges.setdefault((tgt, pol), []).append(e)



        self.edge_index: Dict[str, Edge] = {e["id"]: e for e in ptk["edges"]}

        # direct alias; if you prefer, keep a separate dict with the same type
        self.next_edges: Dict[EdgeKey, List[Edge]] = dict(self.out_edges)

        for (src, pol), arr in self.out_edges.items():
            self.next_edges[(src, pol)] = arr

    @staticmethod
    def edge_key(node_id: Union[str, object], polarity: Union[int, float, object]) -> EdgeKey:
        # coerce node_id to str and polarity to canonical ±1 ints (or just int(polarity) if you prefer)
        nid = str(node_id)
        if isinstance(polarity, float):
            pol_i = 1 if polarity >= 0 else -1
        elif isinstance(polarity, int):
            pol_i = 1 if polarity >= 0 else -1
        else:
            # fall back if something weird sneaks in
            pol_i = 1
        return (nid, pol_i)

    def _edge_gain(self, e):
        typ = e["type"]
        if typ == "within_line":   bias = 1.0
        elif typ == "cross_sutra": bias = 0.9
        elif typ == "special":     bias = 1.2
        else:                      bias = 1.0
        # incorporate flow weight as conductivity
        return bias * float(e["flow"].get("weight", 1.0))

    def _charges_from_node(self, node_id: str) -> Dict[str, float]:
        n = self.nodes[node_id]
        # Simple toy rule-set; customize as needed
        return {
            "line": float(n["line"]),
            "pos": float(n["pos"]),
            "vowel_bias": 1.0 if any(f in n.get("features", []) for f in ["vowel"]) else 0.0
        }

    def simulate_emission(self, positive: List[Sound], negative: List[Sound], cfg: Optional[EmissionConfig]=None):
        if cfg is None:
            cfg = EmissionConfig()

        # Packets: each has (edge_id, progress 0..1, energy, freq, phase, coherence)
        # Start at node; we place them on a virtual 0-length edge and immediately expand along outgoing edges.
        packets = []  # (edge_id, progress, energy, freq, phase, coh)
        def seed_packets(sounds: List[Sound]):
            for s in sounds:
                # Outgoing edges of the matching polarity from the node
                outs = self.next_edges.get((s.node_id, s.polarity), [])
                if not outs:
                    continue
                share = s.energy / len(outs)
                for e in outs:
                    packets.append([e["id"], 0.0, share, s.frequency, s.phase, s.coherence, s.polarity])

        seed_packets(positive)
        seed_packets(negative)

        # For interaction bookkeeping at each time step: map edge_id -> list of packets on it
        particles: List[Particle] = []
        fields: List[Field] = []
        dets: List[DetectionEvent] = []

        def spawn_particle(node_id: str, E: float, coh: float):
            p = Particle(
                id=str(uuid.uuid4()),
                locus=node_id,
                energy=E,
                mass2=E * (0.8 + 0.4*coh),  # toy: coherence lifts effective mass2
                Q=self._charges_from_node(node_id)
            )
            particles.append(p)
            dets.append(DetectionEvent(id=str(uuid.uuid4()), kind="particle", ref_id=p.id, confidence=min(1.0, 0.6+0.4*coh)))

        def spawn_field(edge_ids: List[str], E: float, coh: float):
            f = Field(
                id=str(uuid.uuid4()),
                support_edges=edge_ids[:32],  # cap
                energy=E,
                strength=E * (0.5 + 0.5*coh),
                mode="vector" if coh > 0.7 else "scalar"
            )
            fields.append(f)
            dets.append(DetectionEvent(id=str(uuid.uuid4()), kind="field", ref_id=f.id, confidence=min(1.0, 0.5+0.5*coh)))

        step = 0
        while step < cfg.max_steps and packets and (len(particles)+len(fields) < cfg.max_outputs):
            step += 1

            # Advance packets and apply per-edge gain/decay
            by_edge: Dict[str, List[List[float]]] = {}
            for pk in packets:
                edge_id, prog, E, fr, ph, coh, pol = pk
                e = self.edge_index[edge_id]
                gain = self._edge_gain(e)
                # advance
                prog_new = prog + cfg.step_len
                E_eff = E * gain
                pk[1] = prog_new
                pk[2] = E_eff
                by_edge.setdefault(edge_id, []).append(pk)

            new_packets = []

            # Resolve interactions on each edge
            for edge_id, plist in by_edge.items():
                # split by polarity
                P = [p for p in plist if p[6] == +1]
                N = [p for p in plist if p[6] == -1]

                # Handle cancellations on overlapping segments
                # We approximate: if packets exist of both polarities, cancel a fraction of matched energy
                if P and N:
                    # match by nearest freq & near-antiphase
                    P.sort(key=lambda x: x[3])
                    N.sort(key=lambda x: x[3])
                    i=j=0
                    
                    E_field_accum = 0.0
                    while i < len(P) and j < len(N):
                        p, n = P[i], N[j]
                        df = abs(p[3] - n[3]) / max(1e-6, (p[3] + n[3]) / 2.0)
                        dphi = abs(((p[4] - n[4] + math.pi) % (2*math.pi)) - math.pi)  # wrap to [0,pi]
                        if df <= cfg.cancel_bandwidth and dphi >= (math.pi - cfg.cancel_phase_tol):
                            # amount that cancels is limited by min energy and coherence
                            k = cfg.cancel_efficiency * min(p[5], n[5])
                            dE = k * min(p[2], n[2])
                            p[2] -= dE
                            n[2] -= dE
                            E_field_accum += dE * 0.5  # portion radiates as field
                        # move the pointer with larger frequency to get pairings
                        if p[3] <= n[3]: i += 1
                        else: j += 1

                    # spawn field if meaningful delocalized residual from cancellations
                    if E_field_accum >= cfg.field_E_thresh:
                        # coherent measure = mean coherence of packets encountered
                        coh_vals = [p[5] for p in P+N]
                        coh_mean = sum(coh_vals)/len(coh_vals)
                        spawn_field([edge_id], E_field_accum, coh_mean)

                # Any packet that reached end of edge spawns into outgoing edges of same polarity from target node
                e = self.edge_index[edge_id]
                # target is e['target']
                for pk in plist:
                    edge_id, prog, E, fr, ph, coh, pol = pk
                    if E <= 1e-6:
                        continue
                    if prog < 1.0:
                        # still on the edge
                        new_packets.append(pk)
                    else:
                        # reached end: split to outgoing edges from target
                        #outs = self.next_edges.get((e["target"], pol), [])
                        outs = self.next_edges.get(self.edge_key(e["target"], pol), [])

                        if not outs:
                            # localize energy at node; possible particle
                            if E >= cfg.particle_E_thresh and coh >= cfg.coherence_thresh:
                                spawn_particle(e["target"], E, coh)
                            continue
                        share = (E * cfg.split_decay) / len(outs)
                        for oe in outs:
                            new_packets.append([oe["id"], 0.0, share, fr, ph, coh, pol])

            packets = new_packets

        result = {
            "particles": [asdict(p) for p in particles],
            "fields": [asdict(f) for f in fields],
            "detections": [asdict(d) for d in dets],
            "steps": step
        }
        return result


# ---------- Example usage on your current PTK ----------
with open(ptk_path, "r", encoding="utf-8") as f:
    ptk = json.load(f)

kernel = PTKKernel(ptk)

# Example emission: two lobes (positive starting at n1 and negative starting at n4, same band)
positive = [Sound(node_id="n1", polarity=+1, energy=5.0, frequency=440.0, phase=0.0, coherence=0.9, label="P1")]
negative = [Sound(node_id="n4", polarity=-1, energy=5.0, frequency=440.0, phase=math.pi, coherence=0.9, label="N1")]

res = kernel.simulate_emission(positive, negative, EmissionConfig())
out_json = "ptk_emission_result.json"
with open(out_json, "w", encoding="utf-8") as f:
    json.dump(res, f, indent=2)

print("Wrote", out_json)
print("Particles:", len(res["particles"]), "Fields:", len(res["fields"]), "Detections:", len(res["detections"]))
