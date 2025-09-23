
#[derive(Clone, Debug)]
pub struct PTParams {
    pub alpha_prime: f64,
    pub a_open: f64,
    pub a_closed: f64,
    pub r1: f64,
    pub r2: f64,
    pub c1: f64, pub c2: f64, pub d1: f64, pub d2: f64, // charge map
}

impl Default for PTParams {
    fn default() -> Self {
        Self {
            alpha_prime: 1.0, a_open: 1.0, a_closed: 2.0,
            r1: 1.2, r2: 0.9,
            c1: 1.0/3.0, c2: -1.0/3.0, d1: 0.5, d2: 0.0,
        }
    }
}
