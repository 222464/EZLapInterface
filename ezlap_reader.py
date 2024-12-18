import cp2110
from cp2110 import CP2110Device, UARTConfig, PARITY, FLOW_CONTROL, DATA_BITS, STOP_BITS, RX_TX_MAX
import time
import struct
import sys

# make sure permissions to access /dev/hidraw1 are set to use this!
class EZLapReader:
    def __init__(self):
        try:
            self.ser = CP2110Device(pid=0x86b9)
        except Exception as e:
            print(e)
            print('Could not connect to EZLap!')
            sys.exit(1)

        print("EZLap Connected.")

        self.ser.set_uart_config(UARTConfig(
            baud=38400, parity=PARITY.NONE, flow_control=FLOW_CONTROL.DISABLED,
            data_bits=DATA_BITS.EIGHT, stop_bits=STOP_BITS.SHORT))

        self.ser.enable_uart()

        # init
        self.ser.write([0x03, 0xb9, 0x01])

        self.done = False

        self.buf = bytearray()

    def read(self):
        self.buf += self.ser.read(RX_TX_MAX + 1)

        length = 0
        checksum = 0
        packet_type = 0

        # scan for packet type 132 length 13
        while packet_type != 132 and length != 13 and len(self.buf) > 3:
            self.buf = self.buf[1:] # deplete

            length = int(self.buf[0])
            checksum = int(self.buf[1])
            packet_type = int(self.buf[2])

        if len(self.buf) < 3 or packet_type != 132 or length != 13:
            time.sleep(0.001)
            return None

        # make sure is full
        while len(self.buf) < length and not self.done:
            self.buf += self.ser.read(RX_TX_MAX + 1)
            time.sleep(0.001)

        assert length == 13

        data = self.buf[3:length]

        uid, _, t, hits, signal = struct.unpack('<HHIBB', data)

        self.buf = self.buf[length:] # deplete

        return (uid, t, hits, signal)
            
    def is_open(self):
        return not self.done

    def close(self):
        self.done = True
