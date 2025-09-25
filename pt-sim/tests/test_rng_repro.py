from pt_sim.core.rng import make_rng

def test_rng_determinism():
    r1 = make_rng(42).normal(size=10)
    r2 = make_rng(42).normal(size=10)
    assert (r1 == r2).all()
