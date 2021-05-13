from .power_consumer import PowerConsumer
from .power_source import PowerSource


class PowerBank(PowerSource, PowerConsumer):
    """An object capable of storing energy to later feed other objects."""
    def __init__(self, power_input: int, power_output: int, capacity: int):
        """Initialize the `PowerBank`.

        Args:
            power_input: Specifies the requirement of power for this consumer in watts per second.
                It determines the ratio at which the battery is charged.
            power_output: Total amount of watts per second expended by the battery. It'll drain
                from the stored energy.
            capacity: Total storage capacity of the battery, measured in Joules.
                (1 Joule == 1 Watt/second)
        """
        PowerSource.__init__(self, power_output)
        PowerConsumer.__init__(self, power_input)
        self._stored_power = 0
        self._capacity = capacity

    def capacity(self) -> int:
        """Getter for the total capacity of the battery.

        Returns:
            int: Total storage capacity of the battery, measured in Joules.
                (1 Joule == 1 Watt/second)
        """
        return self._capacity

    def stored_power(self) -> int:
        """Remaining energy on the battery.

        Returns:
            int: Amount of stored energy, measured in Joules.
                (1 Joule == 1 Watt/second)
        """
        return self._stored_power

    def output(self) -> int:
        """Getter for the current output of the battery.

        Returns:
            int: Current output of the battery, in Watts per second. If the stored power is lower
                than the maximum output, it'll be reflected here.
        """
        return min([self.stored_power(), PowerSource.output(self)])

    def max_output(self) -> int:
        """Getter for the mamixum output this battery is capable of.

        Returns:
            int: Maximum output the battery can expend if the stored energy would allow it, in
                Watts per second.
        """
        return PowerSource.output(self)

    def connect(self, consumer: PowerConsumer):
        """Connects the given `PowerConsumer` into this battery's network.

        Args:
            consumer: The object that will start consuming from this battery.

        Returns:
            bool: `True` if it was connected successfully, `False` if the object was already
                connected or if trying to connect the battery to itself.
        """
        return consumer is not self and PowerSource.connect(self, consumer)

    def receive_power(self, watt_amount: int) -> int:
        """Intake power from another source.

        Args:
            watt_amount: Amount of power, in watts, this battery receives during a second span.
                It'll store the energy inside for later usage.

        Returns:
            int: Rounded percentage of efficiency this object has based on the supplied power.
                For example, if the object's input is 100W and the supplied amount is 100W, then
                it'll return 100%. If the supplied amount is 37W, it'll return 37%.
        """
        if self.stored_power() < self.capacity():
            self._stored_power += min([max([watt_amount, self.capacity() - self.stored_power()]), watt_amount])
        return int(watt_amount / self.input() * 100.0)

    def supply_power(self) -> int:
        """Distribute the power output among the connected consumers during one second.

        It'll take the energy out of the storage, reducing its charge. It won't supply 

        Returns:
            int: Amount of power remaining after all consumers took their inputs.
        """
        remaining = self.stored_power()
        if self.stored_power() > 0:
            remaining = PowerSource.supply_power(self)
        self._stored_power -= (self.output() - remaining)
        return remaining
