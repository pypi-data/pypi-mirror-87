# APA102_SPI
Library for controlling APA102 LEDs through any SPI bus.

This library was created because any other library I found couldn't use any SPI bus other than spi0. As the APA102 LEDs don't have a Chip Select, they have to be on a seperate bus without any other devices attached.  
On a Raspberry Pi 4, there are additional SPI busses that can be enabled by appending to `/boot/config.txt`. For example, to enable SPI5:
```
enable_uart=0
dtoverlay=spi5-1cs
```
Here, UART0 has to be disabled, as it shares pins with SPI5.
