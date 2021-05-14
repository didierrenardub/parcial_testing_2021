package ar.edu.ub.testing.power;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertNotEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.util.ArrayList;
import java.util.List;

import org.junit.jupiter.api.Test;

public class PowerSourceTest {

    @Test
    void testOutputInt() {
        PowerSource pow = new PowerSource(100);
        assertEquals(100, pow.output());


    }

    @Test
    void testOutputDifferentInt() {
        PowerSource pow = new PowerSource(50);
        assertNotEquals(10, pow.output());
    }

    @Test
    void testConnect() {
        PowerSource pow = new PowerSource(50);
        array = new ArrayList<PowerConsumer>(); 
        PowerConsumer con = new PowerConsumer(){

            public int input() {
                // TODO Auto-generated method stub
                return 0;
            }

            public int receivePower(int wattAmount) {
                // TODO Auto-generated method stub
                return 0;
            }
            
        };
        array.add(con);
        assertTrue(pow.connect(con));

    }

    @Test
    void testConnectTwosameConsumer() {
        PowerSource pow = new PowerSource(50);
        array = new ArrayList<PowerConsumer>();
        PowerConsumer con = new PowerConsumer(){

            public int input() {
                // TODO Auto-generated method stub
                return 0;
            }

            public int receivePower(int wattAmount) {
                // TODO Auto-generated method stub
                return 0;
            };

        };
        array.add(con);
        array.add(con);
        assertFalse(pow.connect(con));
    }





    private PowerSource pow; 
    private ArrayList<PowerConsumer>array;
}
