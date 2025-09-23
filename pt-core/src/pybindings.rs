
use pyo3::prelude::*;
use pyo3::types::PyModule;


// ----- your pure-Rust function you want to expose -----
fn kk_winding_mass2(level: i32, m: i32, w: i32) -> f64 {
    // placeholder math; replace with your real implementation
    let l = level as f64;
    let mm = m as f64;
    let ww = w as f64;
    l + mm*mm + ww*ww
}


// ----- Python-exposed wrapper -----
#[pyfunction]
fn kk_winding_mass2_py(level: i32, m: i32, w: i32) -> PyResult<f64> {
    Ok(kk_winding_mass2(level, m, w))
}


 

// ----- Module initializer (PyO3 0.22 style) -----
#[pymodule]
fn pt_core_py(_py: Python<'_>, m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(kk_winding_mass2_py, m)?)?;
    Ok(())
}
