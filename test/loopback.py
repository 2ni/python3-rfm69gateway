"""
based on https://gist.github.com/fnishio/b2063941b82f2cf1b935
# loopback test script
# connect MOSI and MISO
"""


import spidev
import time

spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 500000

def BytesToHex(Bytes):
    return ''.join(["0x%02X " % x for x in Bytes]).strip()

try:
    while True:
        resp = spi.xfer([0x01, 0x02])
        print(BytesToHex(resp))
        time.sleep(1)

except KeyboardInterrupt:
    spi.close()
