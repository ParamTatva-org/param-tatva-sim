# Data & IOV (Conditions)

We maintain a sqlite-backed **Conditions DB** keyed by tags and validity intervals (IOVs).  
APIs: `conditions.get(tag, time, key)` with local caching. See Week-2 deliverables.
