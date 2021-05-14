import pytest

from ..power_source import PowerSource
from ..power_consumer import PowerConsumer
from ..power_bank import PowerBank

def test_init():
    pb = PowerBank(100, 200, 2000)

    assert isinstance(pb, PowerBank)

    with pytest.raises(TypeError):
        assert PowerBank()  # pylint: disable=no-value-for-parameter

def test_capacity():
    pb = PowerBank(100, 200, 2000)
    capacity = 2000
    capacity_different = 3000

    assert pb.capacity() == capacity
    assert pb.capacity() != str(capacity)
    assert pb.capacity() != capacity_different

def test_stored_power():
    pb = PowerBank(100, 200, 2000)
    
    assert pb.stored_power() == 0

def test_output():
    pb = PowerBank(100, 200, 2000)

    assert pb.output() == 0

def test_max_output():
    pb = PowerBank(100, 200, 2000)

    assert pb.max_output() == 200

def test_connect():
    pb = PowerBank(100, 200, 2000)
    pb_2 = PowerBank(100, 200, 2000)

    assert not pb.connect(pb)
    assert pb.connect(pb_2)

    with pytest.raises(TypeError):
        assert pb.connect()  # pylint: disable=no-value-for-parameter

    with pytest.raises(TypeError):
        assert pb.connect("i_am_a_bad_string")  # pylint: disable=no-value-for-parameter

def test_receive_power():
    pb = PowerBank(100, 200, 2000)

    assert pb.receive_power(0) == 0
    assert pb.receive_power(50) == 50
    assert pb.receive_power(100) == 100

    with pytest.raises(TypeError):
        assert pb.receive_power()  # pylint: disable=no-value-for-parameter

    with pytest.raises(TypeError):
        assert pb.receive_power("i_am_a_bad_string")  # pylint: disable=no-value-for-parameter

def test_supply_power():
    pb = PowerBank(100, 200, 2000)

    assert pb.supply_power() == 0

    # pc_1 = PowerConsumer(300)
    # pc_2 = PowerConsumer(500)

    # assert pb.connect(pc_1)
    # assert pb.connect(pc_2)

    # assert pb.receive_power(2000)
    # assert pb.supply_power() == 0
