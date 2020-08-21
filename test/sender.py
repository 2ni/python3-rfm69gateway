from etrombly import RFM69
from etrombly.RFM69registers import RF69_868MHZ, REG_VERSION
import RPi.GPIO as GPIO
import time

try:
    radio = RFM69.RFM69(RF69_868MHZ, nodeID=99, networkID=33, isRFM69HW=True)
    results = radio.readAllRegs()
    radio.rcCalibration()
    radio.setHighPower(True)
    print("Radio version: 0x{:02X} frq: {} node:{} network:{} intPin: {} rstPin: {}".format(
        radio.readReg(REG_VERSION),
        radio.freqBand,
        radio.address,
        radio.networkID,
        radio.intPin,
        radio.rstPin
    ))

    while (True):
        gotAck = False
        if radio.send(2, "xx"):
            gotAck = True

        print("Sending... {}".format("ack" if gotAck else "no ack"))

        time.sleep(1)

except KeyboardInterrupt:
    GPIO.cleanup()
except Exception as e:
    print(e)
    GPIO.cleanup()
