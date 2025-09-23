
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
