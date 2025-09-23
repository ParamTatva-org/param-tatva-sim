
use crate::params::PTParams;

/// Toy open-string: m^2 = (N - a_open)/alpha'
pub fn mass2_open(level: u32, p: &PTParams) -> f64 { (level as f64 - p.a_open) / p.alpha_prime }

/// Toy closed-string: m^2 = (N_L + N_R - a_closed)/alpha'
pub fn mass2_closed(level_sum: u32, p: &PTParams) -> f64 { (level_sum as f64 - p.a_closed) / p.alpha_prime }

/// Simple GSO-like level matching: require N_L == N_R (toy)
pub fn level_match_closed(n_left: u32, n_right: u32) -> bool { n_left == n_right }

/// Cartoon spin labels from level
pub fn spin_label_from_level(level: u32) -> i32 {
    match level { 0 => 0, 1 => 1, 2 => 2, _ => 0 }
}
