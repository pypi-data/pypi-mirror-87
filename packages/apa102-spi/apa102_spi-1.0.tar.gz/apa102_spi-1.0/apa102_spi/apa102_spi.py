import numpy as np
import spidev


class APA102:
    START_FRAME = np.array([0x00, 0x00, 0x00, 0x00], dtype=np.uint8)
    @property
    def END_FRAME(self):
        return np.array([0xff] * (self.led_count//8 + 1), dtype=np.uint8)

    def __init__(self, bus, device, led_count, baudrate=500000, spi_mode: int = None):
        self.spi = spidev.SpiDev(bus, device)
        self.spi.max_speed_hz = baudrate
        if spi_mode is not None:
            self.spi.mode = spi_mode
        self.led_count = led_count
        self.pixels = np.zeros((self.led_count, 3), dtype=np.uint8)

    def __getitem__(self, item):
        return self.pixels[item]

    def __setitem__(self, key, value):
        self.pixels[key] = value

    def update(self):
        data = np.full((self.led_count, 4), (0xff, 0, 0, 0), dtype=np.uint8)
        data[:, 1:] = self.pixels[:, ::-1]
        data = np.concatenate([self.START_FRAME, data.flatten(), self.END_FRAME])
        self.spi.writebytes2(data)
