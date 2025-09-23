
use pt_core::potentials::*;

#[test]
fn coulomb_monotonic_decrease() {
    let v1 = coulomb(1.0, 1.0);
    let v2 = coulomb(2.0, 1.0);
    assert!(v2 < v1);
}

#[test]
fn yukawa_monotonic_decrease() {
    let v1 = yukawa(1.0, 1.0, 0.5);
    let v2 = yukawa(2.0, 1.0, 0.5);
    assert!(v2 < v1);
}

#[test]
fn string_linear_increase() {
    let v1 = string_linear(1.0, 0.2, 0.0);
    let v2 = string_linear(2.0, 0.2, 0.0);
    assert!(v2 > v1);
}
