

``` mermaid

  ((Param Tatva ← Maheshvara Sūtras))
    1 · a i u ṇ (it ṇ) (Deva अ इ उ ण) (vowels)
    2 · ṛ ḷ k (it k) (Deva ऋ ऌ क) (vowels)
    3 · e o ṅ (it ṅ) (Deva ए ओ ङ) (vowels)
    4 · ai au c (it c) (Deva ऐ औ च) (vowels)
    5 · ha ya va ra ṭ (it ṭ) (Deva ह य व र ट)
    6 · la ṇ (it ṇ) (Deva ल ण)
    7 · ña ma ṅa ṇa na m (it m) (Deva ञ म ङ ण न म)
    8 · jha bha ñ (it ñ) (Deva झ भ ञ)
    9 · gha ḍha dha ṣ (it ṣ) (Deva घ ढ ध ष)
    10 · ja ba ga ḍa da ś (it ś) (Deva ज ब ग ड द श)
    11 · kha pha cha ṭha tha ca ṭa ta v (it v) (Deva ख फ छ ठ थ च ट त व)
    12 · ka pa y (it y) (Deva क प य)
    13 · śa ṣa sa r (it r) (Deva श ष स र)
    14 · ha l (it l) (Deva ह ल)




```

``` mermaid

flowchart TD
  %% Core
  PT["Param Tatva<br/>built from Maheshwar Sutra"]
  MS["Maheshwar Sūtra — 14 lines"]
  PT --> MS

  %% Line 1
  subgraph L1[1]
    l1a["a"] --> l1i["i"] --> l1u["u"] --> l1N["ṇ"]
  end
  MS --> l1a

  %% Line 2
  subgraph L2[2]
    l2r["ṛ"] --> l2l["ḷ"] --> l2K["k"]
  end
  MS --> l2r

  %% Line 3
  subgraph L3[3]
    l3e["e"] --> l3o["o"] --> l3NG["ṅ"]
  end
  MS --> l3e

  %% Line 4
  subgraph L4[4]
    l4ai["ai"] --> l4au["au"] --> l4C["c"]
  end
  MS --> l4ai

  %% Line 5
  subgraph L5[5]
    l5ha["ha"] --> l5ya["ya"] --> l5va["va"] --> l5ra["ra"] --> l5T["ṭ"]
  end
  MS --> l5ha

  %% Line 6
  subgraph L6[6]
    l6la["la"] --> l6N["ṇ"]
  end
  MS --> l6la

  %% Line 7
  subgraph L7[7]
    l7nya["ña"] --> l7ma["ma"] --> l7nga["ṅa"] --> l7na_dot["ṇa"] --> l7na["na"] --> l7M["m"]
  end
  MS --> l7nya

  %% Line 8
  subgraph L8[8]
    l8jha["jha"] --> l8bha["bha"] --> l8NY["ñ"]
  end
  MS --> l8jha

  %% Line 9
  subgraph L9[9]
    l9gha["gha"] --> l9Dha["ḍha"] --> l9dha["dha"] --> l9SS["ṣ"]
  end
  MS --> l9gha

  %% Line 10
  subgraph L10[10]
    l10ja["ja"] --> l10ba["ba"] --> l10ga["ga"] --> l10Da["ḍa"] --> l10da["da"] --> l10Sh["ś"]
  end
  MS --> l10ja

  %% Line 11
  subgraph L11[11]
    l11kha["kha"] --> l11pha["pha"] --> l11cha["cha"] --> l11Tha["ṭha"] --> l11tha["tha"] --> l11ca["ca"] --> l11Ta["ṭa"] --> l11ta["ta"] --> l11V["v"]
  end
  MS --> l11kha

  %% Line 12
  subgraph L12[12]
    l12ka["ka"] --> l12pa["pa"] --> l12Y["y"]
  end
  MS --> l12ka

  %% Line 13
  subgraph L13[13]
    l13sha["śa"] --> l13ssa["ṣa"] --> l13sa["sa"] --> l13R["r"]
  end
  MS --> l13sha

  %% Line 14
  subgraph L14[14]
    l14ha["ha"] --> l14L["l"]
  end
  MS --> l14ha

  %% Cross-sutra relations (dotted)
  l1N -.-> l7na_dot
  l1N -.-> l4au

  l2K -.-> l12ka
  l2K -.-> l1a

  l3NG -.-> l7ma
  l3NG -.-> l3o

  l4C -.-> l11tha
  l4C -.-> l11kha

  l5T -.-> l11ca
  l5T -.-> l11kha

  l6N -.-> l7na_dot
  l6N -.-> l4au

  l7M -.-> l7nga
  l7M -.-> l7ma

  l8NY -.-> l7na
  l8NY -.-> l7nya

  l9SS -.-> l13ssa
  l9SS -.-> l13sa

  l10Sh -.-> l13sha
  l10Sh -.-> l13sa

  l11V -.-> l5va
  l11V -.-> l5ya

  l12Y -.-> l5ya
  l12Y -.-> l5ra

  l13R -.-> l5ra
  l13R -.-> l5va

  l14L -.-> l6la

  %% Special relation ha (5) -> ha (14) with label
  l5ha -- "special" --> l14ha





```
