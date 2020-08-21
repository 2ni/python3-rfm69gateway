### Description
Gateway running on a Raspberry Pi 4 receiving RFM69 packets, processing them
and sending them to a Home Assistant instance

### Installation
```
sudo apt install python3-venv python3-rpi.gpio
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Debugging SPI
[test](https://www.raspberrypi.org/documentation/hardware/raspberrypi/spi/README.md) if SPI is working:

## Lowlevel testing

```
ll /dev/spidev0.*
wget https://raw.githubusercontent.com/raspberrypi/linux/rpi-3.10.y/Documentation/spi/spidev_test.c
gcc -o spidev_test spidev_test.c
./spidev_test -D /dev/spidev0.0
spi mode: 0
bits per word: 8
max speed: 500000 Hz (500 KHz)

FF FF FF FF FF FF
40 00 00 00 00 95
FF FF FF FF FF FF
FF FF FF FF FF FF
FF FF FF FF FF FF
DE AD BE EF BA AD
F0 0D
```

## Loopback test

Connect MISO with MOSI and run:
```
python test/loopback.py
0x01 0x02
0x01 0x02
...
```

## Test "get current version"

Connect your RFM69 as described in the [library](https://github.com/2ni/RFM69):

| RFM pin | Pi pin
| ------- |-------
| 3v3     | 17
| DIO0    | 18
| MOSI    | 19
| MISO    | 21
| CLK     | 23
| NSS     | 24
| Ground  | 25
| RESET   | 29

```
python test/version.py
all good! Version: 0x24
all good! Version: 0x24
...
```
