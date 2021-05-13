package ar.edu.ub.testing.power;

/** An object capable of storing energy to later feed other objects. */
public class PowerBank extends PowerSource implements PowerConsumer
{
    /** Initialize the `PowerBank`.

    Args:
        powerInput: Specifies the requirement of power for this consumer in watts per second.
            It determines the ratio at which the battery is charged.
        powerOutput: Total amount of watts per second expended by the battery. It'll drain
            from the stored energy.
        capacity: Total storage capacity of the battery, measured in Joules.
            (1 Joule == 1 Watt/second)
    */
    public PowerBank(int powerInput, int powerOutput, int capacity)
    {
        super(powerOutput);
        this.input = powerInput;
        this.capacity = capacity;
        this.storedPower = 0;
    }

    /** Getter for the power intake.

    Returns:
        int: Amount of watts per second the current object consumes.
    */
    public int input()
    {
        return this.input;
    }

    /** Intake power from another source.

    Args:
        wattAmount: Amount of power, in watts, this battery receives during a second span.
            It'll store the energy inside for later usage.

    Returns:
        int: Rounded percentage of efficiency this object has based on the supplied power.
            For example, if the object's input is 100W and the supplied amount is 100W, then
            it'll return 100%. If the supplied amount is 37W, it'll return 37%.
    */
    public int receivePower(int wattAmount)
    {
        if (this.storedPower() < this.capacity())
        {
            this.storedPower += Math.min(wattAmount, this.capacity() - this.storedPower());
        }

        return (int)(wattAmount / this.input() * 100.0f);
    }

    /** Getter for the current output of the battery.

    Returns:
        int: Current output of the battery, in Watts per second. If the stored power is lower
            than the maximum output, it'll be reflected here.
    */
    @Override
    public int output()
    {
        return Math.min(this.storedPower(), super.output());
    }

    /** Connects the given `PowerConsumer` into this battery's network.

    Args:
        consumer: The object that will start consuming from this battery.

    Returns:
        boolean: `true` if it was connected successfully, `false` if the object was already
            connected or if trying to connect the battery to itself.
    */
    @Override
    public boolean connect(PowerConsumer consumer)
    {
        return consumer != this && super.connect(consumer);
    }

    /** Distribute the power output among the connected consumers during one second.

    It'll take the energy out of the storage, reducing its charge. It won't supply 

    Returns:
        int: Amount of power remaining after all consumers took their inputs.
    */
    @Override
    public int supplyPower()
    {
        if (this.storedPower() > 0)
        {
            int remaining = super.supplyPower();
            this.storedPower -= this.output() - remaining;
            return remaining;
        }
        return 0;
    }

    /** Getter for the mamixum output this battery is capable of.

    Returns:
        int: Maximum output the battery can expend if the stored energy would allow it, in
            Watts per second.
    */
    public int maxOutput()
    {
        return super.output();
    }

    /** Getter for the total capacity of the battery.

    Returns:
        int: Total storage capacity of the battery, measured in Joules.
            (1 Joule == 1 Watt/second)
    */
    public int capacity()
    {
        return this.capacity;
    }

    /** Remaining energy on the battery.

    Returns:
        int: Amount of stored energy, measured in Joules.
            (1 Joule == 1 Watt/second)
    */
    public int storedPower()
    {
        return this.storedPower;
    }

    private int input;
    private int capacity;
    private int storedPower;
}
