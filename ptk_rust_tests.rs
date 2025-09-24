use std::fs;
use serde_json::from_str as from_json;
use std::collections::{HashMap, HashSet};

// Adjust imports to your crate path if needed:
// use crate::*; 
// or if placed in a separate crate:
// use param_tatva_kernel::*;

use super::{PTK, EdgeType};

#[test]
fn validate_ptk_kernel() {
    let data = fs::read_to_string("kernel/ptk.v1.json").expect("read ptk.v1.json");
    let ptk: PTK = from_json(&data).expect("valid PTK");

    // Unique node ids
    let mut seen: HashSet<&str> = HashSet::new();
    for n in &ptk.nodes {
        assert!(seen.insert(&n.id), "duplicate node id {}", n.id);
    }

    // Edge references exist and polarity is ±1
    let node_ids: HashSet<_> = ptk.nodes.iter().map(|n| n.id.as_str()).collect();
    for e in &ptk.edges {
        assert!(node_ids.contains(e.source.as_str()), "missing source {}", e.source);
        assert!(node_ids.contains(e.target.as_str()), "missing target {}", e.target);
        assert!(e.polarity == 1 || e.polarity == -1, "polarity must be ±1");
    }

    // Cross/special edges must exist in both polarities
    #[derive(PartialEq, Eq, Hash)]
    struct Key(String,String,String);
    let mut pairs: HashMap<Key, HashSet<i32>> = HashMap::new();
    for e in &ptk.edges {
        match e.edge_type {
            EdgeType::CrossSutra | EdgeType::Special => {
                let (a,b) = if e.source <= e.target { (e.source.clone(), e.target.clone()) } else { (e.target.clone(), e.source.clone()) };
                let t = match e.edge_type {
                    EdgeType::CrossSutra => "cross_sutra".to_string(),
                    EdgeType::Special => "special".to_string(),
                    _ => unreachable!()
                };
                let key = Key(a,b,t);
                pairs.entry(key).or_default().insert(e.polarity);
            }
            _ => {}
        }
    }
    for (_k, pols) in pairs {
        assert!(pols.contains(&1) && pols.contains(&-1), "missing polarity pair");
    }
}
