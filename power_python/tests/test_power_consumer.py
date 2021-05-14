import pytest

from ..power_source import PowerSource
from ..power_consumer import PowerConsumer
from ..power_bank import PowerBank

def test_init():
    pc = PowerConsumer(100)

    assert isinstance(pc, PowerConsumer)

    with pytest.raises(TypeError):
        assert PowerConsumer()  # pylint: disable=no-value-for-parameter

def test_input():
    input = 100
    input_different = 200
    pc = PowerConsumer(100)

    assert pc.input() == input
    assert pc.input() != str(input)
    assert pc.input() != input_different

def test_receive_power():
    with pytest.raises(NotImplementedError):
        pc = PowerConsumer(100)
        pc.receive_power(1)

    with pytest.raises(TypeError):
        pc = PowerConsumer(100)
        pc.receive_power()  # pylint: disable=no-value-for-parameter