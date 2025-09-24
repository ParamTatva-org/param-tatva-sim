Here’s a Mermaid diagram built directly from your attached JSON (nodes grouped by sutra line; solid arrows are within-line order, dashed arrows are cross-sutra references, and the bold arrow is the special ha→ha link):

```mermaid
graph LR
  %% --- Line 1 ---
  subgraph "1"
    n1["a"] --> n2["i"] --> n3["u"] --> n4["Ṇ"]
  end
  %% --- Line 2 ---
  subgraph "2"
    n5["ṛ"] --> n6["ḷ"] --> n7["K"]
  end
  %% --- Line 3 ---
  subgraph "3"
    n8["e"] --> n9["o"] --> n10["Ṅ"]
  end
  %% --- Line 4 ---
  subgraph "4"
    n11["ai"] --> n12["au"] --> n13["C"]
  end
  %% --- Line 5 ---
  subgraph "5"
    n14["ha"] --> n15["ya"] --> n16["va"] --> n17["ra"] --> n18["Ṭ"]
  end
  %% --- Line 6 ---
  subgraph "6"
    n19["la"] --> n20["Ṇ"]
  end
  %% --- Line 7 ---
  subgraph "7"
    n21["ña"] --> n22["ma"] --> n23["ṅa"] --> n24["ṇa"] --> n25["na"] --> n26["M"]
  end
  %% --- Line 8 ---
  subgraph "8"
    n27["jha"] --> n28["bha"] --> n29["Ñ"]
  end
  %% --- Line 9 ---
  subgraph "9"
    n30["gha"] --> n31["ḍha"] --> n32["dha"] --> n33["Ṣ"]
  end
  %% --- Line 10 ---
  subgraph "10"
    n34["ja"] --> n35["ba"] --> n36["ga"] --> n37["ḍa"] --> n38["da"] --> n39["Ś"]
  end
  %% --- Line 11 ---
  subgraph "11"
    n40["kha"] --> n41["pha"] --> n42["cha"] --> n43["ṭha"] --> n44["tha"] --> n45["ca"] --> n46["ṭa"] --> n47["ta"] --> n48["V"]
  end
  %% --- Line 12 ---
  subgraph "12"
    n49["ka"] --> n50["pa"] --> n51["Y"]
  end
  %% --- Line 13 ---
  subgraph "13"
    n52["śa"] --> n53["ṣa"] --> n54["sa"] --> n55["R"]
  end
  %% --- Line 14 ---
  subgraph "14"
    n56["ha"] --> n57["L"]
  end

  %% Cross-sutra (dashed)
  n4 -.-> n24
  n7 -.-> n49
  n10 -.-> n23
  n13 -.-> n45
  n18 -.-> n46
  n20 -.-> n24
  n26 -.-> n22
  n29 -.-> n21
  n33 -.-> n53
  n39 -.-> n52
  n48 -.-> n16
  n51 -.-> n15
  n55 -.-> n17
  n57 -.-> n19

  %% Special ha (bold)
  n14 ==> n56
```

