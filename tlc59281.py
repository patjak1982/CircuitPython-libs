import busio
import digitalio


class TLC59281:
    def __init__(
        self, spi: busio.SPI,
            latch: digitalio.DigitalInOut) -> None:
        self._spi = spi
        self._latch = latch
        self._latch.switch_to_output(value=False)
        self._shift_reg = bytearray(2)
        self.write()

    def write(self) -> None:
        # Write out the current state to the shift register.
        try:
            # Lock the SPI bus and configure it for the shift register.
            while not self._spi.try_lock():
                pass

            # First ensure latch is low.
            self._latch.value = False
            # Write out the bits.
            self._spi.write(self._shift_reg, start=0, end=1)
            # Then toggle latch high and low to set the value.
            self._latch.value = True
            self._latch.value = False
        finally:
            # Ensure the SPI bus is unlocked.
            self._spi.unlock()

    def setPin(self, pin: int, value: int) -> None:
        byteindex = int(pin / 8)
        bitinbyte = pin % 8
        if value == 0:
            self._shift_reg[byteindex] &= ~(1 << bitinbyte)
        else:
            self._shift_reg[byteindex] |= (1 << bitinbyte)
