
use pt_core::compact::*;

#[test]
fn kk_symmetry_sign_momentum() {
    // m^2 should be even in m1, m2 (depends on squares)
    let a = kk_winding_mass2( 1, -2, 0, 0, 1.2, 0.9, 1.0);
    let b = kk_winding_mass2(-1,  2, 0, 0, 1.2, 0.9, 1.0);
    assert!((a - b).abs() < 1e-12);
}

#[test]
fn kk_increases_with_winding() {
    let a = kk_winding_mass2(0,0,0,0,1.2,0.9,1.0);
    let b = kk_winding_mass2(0,0,1,0,1.2,0.9,1.0);
    assert!(b > a);
}
