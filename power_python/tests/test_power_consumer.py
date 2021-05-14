
from ..power_consumer import PowerConsumer

def test_consumer():
    c = PowerConsumer()
    assert c.consumer() == 200

