package ar.edu.ub.testing.power;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertNotEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

import org.junit.jupiter.api.Test;

public class PowerBankTest {

    @Test
    void testInputInt() {
        PowerBank pow = new PowerBank(50, 20, 150);
        assertEquals(50, pow.input());
    }

    @Test
    void testInputDiferentInt() {
        PowerBank pow = new PowerBank(50, 20, 150);
        assertNotEquals(10, pow.input());
    }

    @Test
    void testReceivePowerWrong() {
        PowerBank pow = new PowerBank(50, 20, -150);
        pow.storedPower();
        assertNotEquals(300, pow.receivePower(100));

    }

    @Test
    void testReceivePower() {
        PowerBank pow = new PowerBank(50, 20, 200);
        pow.storedPower();
        assertEquals(150, pow.receivePower(150));

    }

    @Test
    void testOutput() {
        PowerBank pow = new PowerBank(50, 40, 100);
        pow.storedPower();
        pow.output();
        assertTrue(pow.storedPower()< pow.output());
    }

    @Test
    void testSupplyPower() {
        PowerBank pow = new PowerBank(50, 40, 100);
        pow.storedPower();
        assertTrue(pow.storedPower() <= 0);

    }

    
}
