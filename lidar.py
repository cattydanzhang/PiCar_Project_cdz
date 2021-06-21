import sys
import smbus
import time

class LidarLite:
    _LIDAR_ADR=0x62

    def __init__(self):
        self._bus = smbus.SMBus(1)
    def measure(self):
        self._bus.write_byte_data(self._LIDAR_ADR,0,4)
        self._bus.write_byte(self._LIDAR_ADR, 1)
        while self._bus.read_byte(self._LIDAR_ADR) & 1 != 0:
            pass
        self._bus.write_byte(self._LIDAR_ADR, 0xf)
        d=self._bus.read_byte(self._LIDAR_ADR)<<8
        self._bus.write_byte(self._LIDAR_ADR, 0x10)
        d|=self._bus.read_byte(self._LIDAR_ADR)
        return d
