# Param Tatva from Maheshwara Sutras

A full Markdown explainer showing how Param Tatva emerges from the **14 Maheshwara Sutras**, with **two levels of continuation**:

1. **Primary Continuation (Prathama Srota)** – Each sutra’s **anubandha** (marker) links to the **first sound of the next sutra**.
2. **Secondary Continuation (It-Pratyaya Srota)** – Each sutra’s **anubandha** connects to specific other sutra positions. The mapping is explicit and finite.

---

## Secondary Continuation Mapping

According to the system:

* 1‑4 (ṇ) → 7‑4 (ṇa)
* 2‑3 (k) → 12‑1 (ka)
* 3‑3 (ṅ) → 7‑3 (ṅa)
* 4‑3 (c) → 11‑6 (ca)
* 5‑5 (ṭ) → 11‑7 (ṭa)
* 6‑2 (ṇ) → 7‑4 (ṇa)
* 7‑6 (m) → 7‑2 (ma)
* 8‑3 (ñ) → 7‑1 (ña)
* 9‑4 (ṣ) → 13‑2 (ṣa)
* 10‑6 (ś) → 13‑1 (śa)
* 11‑9 (v) → 5‑3 (va)
* 12‑3 (y) → 5‑2 (ya)
* 13‑4 (r) → 5‑4 (ra)
* (5)14‑2 (l) → 6‑1 (la)

---

## Overview (Mindmap)

```mermaid
mindmap
  root((Param Tatva))
    Sutra 1: a i u ṇ
      a
      i
      u
      ṇ (→ Sutra 2, and → 7‑4 ṇa)
    Sutra 2: ṛ ḷ k
      ṛ
      ḷ
      k (→ Sutra 3, and → 12‑1 ka)
    Sutra 3: e o ṅ
      e
      o
      ṅ (→ Sutra 4, and → 7‑3 ṅa)
    Sutra 4: ai au c
      ai
      au
      c (→ Sutra 5, and → 11‑6 ca)
    Sutra 5: ha ya va ra ṭ
      ha
      ya
      va
      ra
      ṭ (→ Sutra 6, and → 11‑7 ṭa)
    Sutra 6: la ṇ
      la
      ṇ (→ Sutra 7, and → 7‑4 ṇa)
    Sutra 7: ña ma ṅa ṇa na m
      ña (target of 8‑3)
      ma (target of 7‑6)
      ṅa (target of 3‑3)
      ṇa (target of 1‑4, 6‑2)
      na
      m (→ Sutra 8)
    Sutra 8: jha bha ñ
      jha
      bha
      ñ (→ Sutra 9, and → 7‑1 ña)
    Sutra 9: gha ḍha dha ṣ
      gha
      ḍha
      dha
      ṣ (→ Sutra 10, and → 13‑2 ṣa)
    Sutra 10: ja ba ga ḍa da ś
      ja
      ba
      ga
      ḍa
      da
      ś (→ Sutra 11, and → 13‑1 śa)
    Sutra 11: kha pha cha ṭha tha ca ṭa ta v
      kha
      pha
      cha
      ṭha
      tha
      ca (target of 4‑3)
      ṭa (target of 5‑5)
      ta
      v (→ Sutra 12, and → 5‑3 va)
    Sutra 12: ka pa y
      ka (target of 2‑3)
      pa
      y (→ Sutra 13, and → 5‑2 ya)
    Sutra 13: śa ṣa sa r
      śa (target of 10‑6)
      ṣa (target of 9‑4)
      sa
      r (→ Sutra 14, and → 5‑4 ra)
    Sutra 14: ha l
      ha
      l (→ END, and → 6‑1 la)
```

---

## Full Sequence (Flowchart with Dual Continuation)

```mermaid
graph TD
  classDef marker fill:#f9f9f9,stroke:#bbb,stroke-dasharray:4 2;
  classDef second stroke:#ff3333,stroke-width:2px;

  %% Only showing continuation highlights
  m1[1‑4 ṇ]:::marker --> a4[2‑1 ṛ]
  m1 -.-> n7d[7‑4 ṇa]:::second

  m2[2‑3 k]:::marker --> a6[3‑1 e]
  m2 -.-> k12[12‑1 ka]:::second

  m3[3‑3 ṅ]:::marker --> a8[4‑1 ai]
  m3 -.-> n7c[7‑3 ṅa]:::second

  m4[4‑3 c]:::marker --> h5[5‑1 ha]
  m4 -.-> c11[11‑6 ca]:::second

  m5[5‑5 ṭ]:::marker --> l6[6‑1 la]
  m5 -.-> t11r[11‑7 ṭa]:::second

  m6[6‑2 ṇ]:::marker --> n7a[7‑1 ña]
  m6 -.-> n7d[7‑4 ṇa]:::second

  m7[7‑6 m]:::marker --> j8[8‑1 jha]
  m7 -.-> n7b[7‑2 ma]:::second

  m8[8‑3 ñ]:::marker --> g9[9‑1 gha]
  m8 -.-> n7a[7‑1 ña]:::second

  m9[9‑4 ṣ]:::marker --> j10[10‑1 ja]
  m9 -.-> s13r[13‑2 ṣa]:::second

  m10[10‑6 ś]:::marker --> kh11[11‑1 kha]
  m10 -.-> s13p[13‑1 śa]:::second

  m11[11‑9 v]:::marker --> k12[12‑1 ka]
  m11 -.-> v5[5‑3 va]:::second

  m12[12‑3 y]:::marker --> s13p[13‑1 śa]
  m12 -.-> y5[5‑2 ya]:::second

  m13[13‑4 r]:::marker --> h14[14‑1 ha]
  m13 -.-> r5[5‑4 ra]:::second

  m14[14‑2 l]:::marker --> END[END]
  m14 -.-> l6[6‑1 la]:::second
```

---

## Notes

* **Primary Continuity**: as before, anubandhas → first sound of next sutra.
* **Secondary Continuity**: now mapped explicitly per the tradition (see mapping list).
* Sutras 5 and 14 overlap in “ha” and “la”, creating a cyclic loop.
* This dual layering reflects **cyclic resonance** of sounds in Param Tatva.
* Sutra 7 has a self-loop as well.
* Sutra 5-11 also creates a larger loop.

