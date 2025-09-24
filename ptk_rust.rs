use serde::{Deserialize, Serialize};

#[derive(Debug, Serialize, Deserialize)]
pub struct Flow {
    pub dash: (u32, u32),
    pub speed: f64,
    pub weight: f64,
}

#[derive(Debug, Serialize, Deserialize)]
#[serde(rename_all = "snake_case")]
pub enum EdgeType {
    WithinLine,
    CrossSutra,
    Special,
}

#[derive(Debug, Serialize, Deserialize)]
pub struct Node {
    pub id: String,
    pub label: String,
    pub sanskrit: Option<String>,
    pub line: u32,
    pub pos: u32,
    pub features: Vec<String>,
}

#[derive(Debug, Serialize, Deserialize)]
pub struct Edge {
    pub id: String,
    pub source: String,
    pub target: String,
    #[serde(rename = "type")]
    pub edge_type: EdgeType,
    pub polarity: i32,
    pub flow: Flow,
}

#[derive(Debug, Serialize, Deserialize)]
pub struct Group {
    pub name: String,
    pub key: serde_json::Value,
    pub node_ids: Vec<String>,
}

#[derive(Debug, Serialize, Deserialize)]
pub struct PTK {
    pub ptk_version: String,
    pub universe: String,
    pub meta: serde_json::Value,
    pub nodes: Vec<Node>,
    pub edges: Vec<Edge>,
    pub groups: Vec<Group>,
    pub render_hints: serde_json::Value,
}
