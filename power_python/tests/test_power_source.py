import pytest

from ..power_source import PowerSource
from ..power_consumer import PowerConsumer
from ..power_bank import PowerBank


def test_init():
    ps = PowerSource(2000)

    assert isinstance(ps, PowerSource)

    with pytest.raises(TypeError):
        assert PowerSource()  # pylint: disable=no-value-for-parameter

def test_output():
    output = 2000
    output_different = 3000
    ps = PowerSource(2000)

    assert ps.output() == output
    assert ps.output() != str(output)
    assert ps.output() != output_different

def test_connect():
    ps = PowerSource(2000)
    pc = PowerConsumer(100)

    assert ps.connect(pc)
    assert not ps.connect(pc)
    
def test_supply_power():
    ps = PowerSource(2000)
    pb = PowerBank(100, 2000, 10000)
    ps.connect(pb)

    with pytest.raises(NotImplementedError):
        ps_temp = PowerSource(2000)
        pc_temp = PowerConsumer(100)
        ps_temp.connect(pc_temp)
        ps_temp.supply_power()

    assert ps.supply_power() == 1900
