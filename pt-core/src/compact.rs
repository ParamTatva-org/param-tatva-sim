
/// KK + winding contributions on a 2-torus with radii r1, r2 (toy).
pub fn kk_winding_mass2(m1:i32,m2:i32,w1:i32,w2:i32,r1:f64,r2:f64,alpha_prime:f64)->f64{
    let kk=(m1 as f64 / r1).powi(2) + (m2 as f64 / r2).powi(2);
    let wind=((w1 as f64)*r1/alpha_prime).powi(2) + ((w2 as f64)*r2/alpha_prime).powi(2);
    kk+wind
}

/// Linear charge-like map
pub fn charge_linear_map(m1:i32,m2:i32,w1:i32,w2:i32,c1:f64,c2:f64,d1:f64,d2:f64)->f64{
    c1*(m1 as f64)+c2*(m2 as f64)+d1*(w1 as f64)+d2*(w2 as f64)
}
