import time
import spidev
import RPi.GPIO as GPIO
from RFM69.registers import REG_VERSION

"""
default values
they are handled by rpi
no need to set them up
with GPIO
3.3v 17
GND  20 or 25
"""
MOSI = 19
MISO = 21
SCK = 23
CS = 24  # CE0 for device 0, CE1 = 26 for device 1
RST = 29
DIO0 = 18

spi = spidev.SpiDev()
spi.open(0, 0)  # bus, device
spi.max_speed_hz = 8000000
spi.mode = 0b00

GPIO.setmode(GPIO.BOARD)

# reset procedure (possibly not needed)
GPIO.setup(RST, GPIO.OUT)
GPIO.output(RST, GPIO.HIGH)
time.sleep(0.1)
GPIO.output(RST, GPIO.LOW)
time.sleep(0.1)

GPIO.setup(CS, GPIO.OUT)
GPIO.output(CS, GPIO.HIGH)


def read_reg(addr):
    GPIO.output(CS, GPIO.LOW)
    value = spi.xfer([addr & 0x7F, 0])[1]
    GPIO.output(CS, GPIO.HIGH)

    return value


try:
    while True:
        version = read_reg(REG_VERSION)
        if version == 0x24:
            print("all good! Version: 0x{:02X}".format(version))
        else:
            print("meh. Version: 0x{:02X} (expected 0x24)".format(version))
        time.sleep(1)

except KeyboardInterrupt:
    spi.close()
    GPIO.cleanup()
except Exception as e:
    print(e)
    spi.close()
    GPIO.cleanup()

"""
try:
    while True:
        print(spi.xfer([15]))
        time.sleep(1)

except KeyboardInterrupt:
    spi.close()
"""
