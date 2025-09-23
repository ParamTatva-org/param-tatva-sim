
use crate::{PTParams, spectrum::mass2_open, compact::{kk_winding_mass2, charge_linear_map}};

#[derive(Clone, Debug)]
pub struct StateSpec {
    pub level: u32,
    pub m1: i32, pub m2: i32, pub w1: i32, pub w2: i32,
    pub mass: f64, pub q: f64,
}

/// Enumerate open-string states (toy) over level and (m,w) ranges; drop tachyonic m^2 < 0.
pub fn enumerate_states(p: &PTParams, levels: std::ops::RangeInclusive<u32>,
                        m_range: std::ops::RangeInclusive<i32>,
                        w_range: std::ops::RangeInclusive<i32>) -> Vec<StateSpec> {
    let mut out = Vec::new();
    for l in levels {
        let m2_osc = mass2_open(l, p);
        for m1 in m_range.clone() {
            for m2 in m_range.clone() {
                for w1 in w_range.clone() {
                    for w2 in w_range.clone() {
                        let m2c = kk_winding_mass2(m1, m2, w1, w2, p.r1, p.r2, p.alpha_prime);
                        let m2t = m2_osc + m2c;
                        if m2t < 0.0 { continue; }
                        let mass = m2t.sqrt();
                        let q = charge_linear_map(m1, m2, w1, w2, p.c1, p.c2, p.d1, p.d2);
                        out.push(StateSpec { level: l, m1, m2, w1, w2, mass, q });
                    }
                }
            }
        }
    }
    out
}
