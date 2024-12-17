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
        #self.ser.write([0x03, 0xb9, 0x01])

        self.done = False

    def read(self):
        buf = []
        chunk = self.ser.read(RX_TX_MAX + 1)

        while chunk and not self.done:
            buf += chunk
            time.sleep(0.025)
            chunk = self.ser.read(RX_TX_MAX + 1)

        if self.done or len(buf) == 0:
            return None

        length = int(buf[0])
        checksum = int(buf[1])
        packet_type = buf[2]

        if packet_type == b'\x84': # lap packet
            assert length == 13

            data = buf[3:]

            uid, _, t, hits, signal = struct.unpack(buf, '<HHIBB')

            return (uid, t, hits, signal)

        return None
            
    def is_open(self):
        return not self.done

    def close(self):
        self.done = True
