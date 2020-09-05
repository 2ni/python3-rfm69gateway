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

        """
        print("'{data}' from 0x{sender:04x}. RSSI: {rssi}".format(
            data="".join([chr(letter) for letter in radio.DATA]),
            sender=radio.SENDERID,
            rssi=radio.RSSI)
        )
        """

        # data conists of chunks of 4 bytes: 2 bytes cmd name, 2 bytes value
        i = 0
        data = {}
        while i < len(radio.DATA):
            cmd = "".join(chr(letter) for letter in radio.DATA[i:i + 2])
            value = (radio.DATA[i + 2] << 8) | radio.DATA[i + 3]
            i += 4
            data[cmd] = value

        sender = radio.SENDERID
        rssi = radio.RSSI

        if radio.ACKRequested():
            radio.sendACK(sender, dt.now().strftime("%Y-%m-%d %H:%M:%S"))  # return the current timestamp to the sender

        # process received data
        print("data from 0x{sender:2x} [RSSI: {rssi}]".format(sender=sender, rssi=rssi))
        for k, v in data.items():
            print("{k}: {v}".format(k=k, v=v))

except KeyboardInterrupt:
    radio.shutdown()
except Exception as e:
    print(e)
    radio.shutdown()
