
pub fn coulomb(r:f64, alpha:f64)->f64{ let r=if r.abs()<1e-9 {1e-9} else {r}; alpha/r }
pub fn yukawa(r:f64, g:f64, m:f64)->f64{ let r=if r.abs()<1e-9 {1e-9} else {r}; (g*g)*(-m*r).exp()/r }
pub fn string_linear(r:f64, kappa:f64, c:f64)->f64{ kappa*r + c }
