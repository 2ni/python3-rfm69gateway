from pyrfm69 import RFM69
from pyrfm69.RFM69registers import RF69_868MHZ, REG_VERSION
import time
from datetime import datetime as dt

radio = RFM69.RFM69(RF69_868MHZ, nodeID=99, networkID=33, isRFM69HW=True)
radio.setHighPower(True)

try:
    print("Radio version: 0x{:02X} frq: {} node:{} network:{} intPin: {} rstPin: {}".format(
        radio.readReg(REG_VERSION),
        radio.freqBand,
        radio.address,
        radio.networkID,
        radio.intPin,
        radio.rstPin
    ))

    while True:
        radio.receiveBegin()
        while not radio.receiveDone():
            time.sleep(.1)

        print("'%s' from %s RSSI:%s" % ("".join([chr(letter) for letter in radio.DATA]), radio.SENDERID, radio.RSSI))
        sender = radio.SENDERID
        if radio.ACKRequested():
            radio.sendACK(sender, dt.now().strftime("%Y-%m-%d %H:%M:%S"))  # return the current datestamp to the sender

except KeyboardInterrupt:
    radio.shutdown()
except Exception as e:
    print(e)
    radio.shutdown()
