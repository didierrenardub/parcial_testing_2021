package ar.edu.ub.testing.power;


/** Interface for power consuming objects. */
public interface PowerConsumer
{
    /** Getter for the power intake.

    Returns:
        int: Amount of watts per second the current object consumes.
    */
    int input();

    /** Powers the current object.

    Args:
        wattAmount: Amount of power, in watts, this object receives during a second span.

    Returns:
        int: Rounded percentage of efficiency this object has based on the supplied power.
            For example, if the object's input is 100W and the supplied amount is 100W, then
            it'll return 100%. If the supplied amount is 37W, it'll return 37%.
    */
    int receivePower(int wattAmount);
}
