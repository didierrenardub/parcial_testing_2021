

class PowerConsumer():
    """Base class for power consuming objects."""
    def __init__(self, power_input: int):
        """Initialize the `PowerConsumer` object.

        Args:
            power_input: Specifies the requirement of power for this consumer in watts per second.
        """
        self._input = power_input

    def input(self) -> int:
        """Getter for the power intake.

        Returns:
            int: Amount of watts per second the current object consumes.
        """
        return self._input

    def receive_power(self, watt_amount: int) -> int:
        """Definition of the signature for this object to be powered.

        Args:
            watt_amount: Amount of power, in watts, this object receives during a second span.

        Returns:
            int: Rounded percentage of efficiency this object has based on the supplied power.
                For example, if the object's input is 100W and the supplied amount is 100W, then
                it'll return 100%. If the supplied amount is 37W, it'll return 37%.

        Raises:
            NotImplementedError: This method is meant to be implemented by derived classes.
        """
        raise NotImplementedError()
