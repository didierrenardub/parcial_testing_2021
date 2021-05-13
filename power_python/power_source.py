from .power_consumer import PowerConsumer


class PowerSource():
    """A power supplier class."""
    def __init__(self, power_output: int):
        """Initialize the `PowerSource`.

        Args:
            power_output: Total amount of watts per second expended by the power source.
        """
        self._output = power_output
        self._connections = []

    def output(self) -> int:
        """Getter for the maximum supplied power.
        
        Returns:
            int: Amount of watts per second supplied to the objects connected to the network.
        """
        return self._output

    def connect(self, consumer: PowerConsumer) -> bool:
        """Connects the given `PowerConsumer` into this source's network.

        Args:
            consumer: The object that will start consuming from this supplier.

        Returns:
            bool: `True` if it was connected successfully, `False` if the object was already
                connected.
        """
        if consumer not in self._connections:
            self._connections.append(consumer)
            return True
        return False

    def supply_power(self) -> int:
        """Distribute the power output among the connected consumers during one second.

        Returns:
            int: Amount of power remaining after all consumers took their inputs.
        """
        remaining_power = self.output()
        for consumer in self._connections:
            supply = min([remaining_power, consumer.input()])
            consumer.receive_power(supply)
            remaining_power -= supply
        return remaining_power
