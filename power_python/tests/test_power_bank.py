from power_python.power_consumer import PowerConsumer
from ..power_source import PowerSource
from ..power_bank import PowerBank

def test_power_bank():
    power_bank = (PowerBank(150, 150, 3000))
    assert power_bank.capacity() == 3000
    assert power_bank.max_output() == 150
    assert power_bank.output() == 0
    power_source = PowerSource(150)
    assert power_source.connect(power_bank) == True
    assert power_bank.receive_power(power_source.output()) == 100
    assert power_bank.stored_power() == 150
    assert power_bank.output() == 150
    consumer = PowerBank(100, 100, 1000)
    assert power_bank.connect(consumer) == True
    assert power_bank.connect(consumer) == False
    assert power_bank.supply_power() == 50




