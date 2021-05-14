from ..power_source import PowerSource
from ..power_bank import PowerBank


# def test_example():
#     p = PowerSource(300)
#     assert p.output() == 300
#     assert p.supply_power() == p.output()
#     b = PowerBank(150, 150, 3000)
#     assert b.capacity() == 3000 and b.input() == 150 and b.output() == 0
#     assert p.connect(b) and not p.connect(b)
#     assert p.supply_power() == p.output() - b.input() and b.output() == 150


def test_power_source():
    power_source = PowerSource(100)
    assert power_source.output() == 100
    assert power_source.supply_power() == power_source.output() 
    power_bank = PowerBank(50, 50, 1000)
    assert power_source.connect(power_bank) == True
    assert power_source.supply_power() == 50
    assert power_bank.stored_power() == 50
    assert power_source.connect(power_bank) == False

