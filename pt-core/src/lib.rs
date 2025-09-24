
pub mod params;
pub mod spectrum;
pub mod compact;
pub mod potentials;
pub mod utils;
pub mod states;

// Re-exports
pub use params::PTParams;
pub use spectrum::{mass2_open, mass2_closed, spin_label_from_level, level_match_closed};
pub use compact::{kk_winding_mass2, charge_linear_map};
pub use potentials::{coulomb, yukawa, string_linear};
pub use states::{StateSpec, enumerate_states};

// Python bindings (optional feature)
#[cfg(feature = "python")]
mod pybindings;


use pyo3::prelude::*;

#[pyfunction]
fn kk_winding_mass2_py(m1: i64, m2: i64, w1: i64, w2: i64, r1: f64, r2: f64, alpha_prime: f64) -> PyResult<f64> {
    let term = (m1 as f64 / r1).powi(2) + (m2 as f64 / r2).powi(2)
        + ((w1 as f64) * r1 / alpha_prime).powi(2)
        + ((w2 as f64) * r2 / alpha_prime).powi(2);
    Ok(term)
}

#[pyfunction]
fn boris_step_py(q_over_m: f64, dt: f64, v: (f64,f64,f64), e: (f64,f64,f64), b: (f64,f64,f64), gamma: f64) -> PyResult<(f64,f64,f64)> {
    let (vx,vy,vz) = v; let (ex,ey,ez) = e; let (bx,by,bz) = b;
    // half E-kick
    let vmx = vx + q_over_m*ex*dt*0.5/gamma;
    let vmy = vy + q_over_m*ey*dt*0.5/gamma;
    let vmz = vz + q_over_m*ez*dt*0.5/gamma;
    // t vector
    let tx = q_over_m*bx*dt*0.5/gamma;
    let ty = q_over_m*by*dt*0.5/gamma;
    let tz = q_over_m*bz*dt*0.5/gamma;
    // v' = v- + v- x t
    let vpx = vmx + (vmy*tz - vmz*ty);
    let vpy = vmy + (vmz*tx - vmx*tz);
    let vpz = vmz + (vmx*ty - vmy*tx);
    // s = 2t/(1+t^2)
    let t2 = tx*tx + ty*ty + tz*tz;
    let sx = 2.0*tx/(1.0+t2);
    let sy = 2.0*ty/(1.0+t2);
    let sz = 2.0*tz/(1.0+t2);
    // v+ = v- + v' x s
    let vpxs_x = vpy*sz - vpz*sy;
    let vpxs_y = vpz*sx - vpx*sz;
    let vpxs_z = vpx*sy - vpy*sx;
    let vpx_ = vmx + vpxs_x;
    let vpy_ = vmy + vpxs_y;
    let vpz_ = vmz + vpxs_z;
    // half E-kick
    let vnx = vpx_ + q_over_m*ex*dt*0.5/gamma;
    let vny = vpy_ + q_over_m*ey*dt*0.5/gamma;
    let vnz = vpz_ + q_over_m*ez*dt*0.5/gamma;
    Ok((vnx,vny,vnz))
}

#[pymodule]
fn pt_core_py(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(kk_winding_mass2_py, m)?)?;
    m.add_function(wrap_pyfunction!(boris_step_py, m)?)?;
    Ok(())
}
