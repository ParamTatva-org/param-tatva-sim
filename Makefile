.PHONY: all viz animate detect validate test
all: validate test viz detect

validate:
\tpython ptk_pydantic_validator.py ptk.v1.json

viz:
\tpython gen__kernel_viz.py

animate:
\tpython gen__kernel_anime.py

emit:
\tpython tools/run_emission.py \
\t  --positive '[{"node_id":"n1","polarity":1,"energy":5,"frequency":440,"phase":0,"coherence":0.9}]' \
\t  --negative '[{"node_id":"n4","polarity":-1,"energy":5,"frequency":440,"phase":3.14159,"coherence":0.9}]' \
\t  --out out/ptk_emission_result.json

detect: emit
\tpython -m pt_sim.detector.run_from_kernel

test:
\tpytest -q
