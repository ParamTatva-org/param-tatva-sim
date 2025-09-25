from pt_sim.core.ledger import Ledger

def test_ledger_basic():
    L = Ledger()
    L.add(energy_in=100.0)
    L.add(energy_out=95.0, energy_field=3.0, energy_particles=2.0)
    L.add(charge_in=1.0, charge_out=1.0)
    L.assert_within(energy_tol=0.05, charge_tol=1e-9)
