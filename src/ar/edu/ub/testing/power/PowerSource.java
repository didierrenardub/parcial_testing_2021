package ar.edu.ub.testing.power;
import java.util.ArrayList;

/** A power supplier class. */
public class PowerSource
{
    /** Initialize the `PowerSource`.

    Args:
        powerOutput: Total amount of watts per second expended by the power source.
    */
    public PowerSource(int powerOutput)
    {
        this.output = powerOutput;
    }

    /** Getter for the maximum supplied power.
        
    Returns:
        int: Amount of watts per second supplied to the objects connected to the network.
    */
    public int output()
    {
        return this.output;
    }

    /** Connects the given `PowerConsumer` into this source's network.

    Args:
        consumer: The object that will start consuming from this supplier.

    Returns:
        boolean: `true` if it was connected successfully, `false` if the object was already
            connected.
    */
    public boolean connect(PowerConsumer consumer)
    {
        if (!this.connections.contains(consumer))
        {
            this.connections.add(consumer);
            return true;
        }

        return false;
    }

    /** Distribute the power output among the connected consumers during one second.

    Returns:
        int: Amount of power remaining after all consumers took their inputs.
    */
    public int supplyPower()
    {
        int remainingPower = this.output();
        for (PowerConsumer consumer : this.connections)
        {
            int supply = Math.min(remainingPower, consumer.input());
            consumer.receivePower(supply);
            remainingPower -= supply;
        }
        return remainingPower;
    }

    private ArrayList<PowerConsumer> connections;
    private int output;
}
