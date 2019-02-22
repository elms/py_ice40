import array
import periphery
import pylibftdi

import sys
import time


class SpiNotImplemented(Exception):
    pass


class spi_interface:
    def __init__(self, speed, mode, **kwargs):
        pass

    def __enter__(self):
        return self

    def __exit__(self, dtype, value, traceback):
        return self.close()

    def transfer(self, data):
        raise SpiNotImplemented()

    def close(self):
        raise SpiNotImplemented()


SpiDev = periphery.SPI

BITMODE_MPSEE = 0x2

MC_SETB_LOW = 0x80
MC_TCK_D5 = 0x8B
MC_SET_CLK_DIV = 0x86

MC_DATA_TMS = 0x40
MC_DATA_IN = 0x20
MC_DATA_OUT = 0x10
MC_DATA_LSB = 0x08
MC_DATA_ICN = 0x04
MC_DATA_BITS = 0x02
MC_DATA_OCN = 0x01

from ctypes import byref, create_string_buffer


class spi_ftdi(spi_interface):
    def __init__(self, speed, mode, interface=None, **kwargs):
        self.speed = speed
        self.mode = mode

        self.dev = pylibftdi.Device(interface_select=interface, **kwargs)

        self._open()

    def __del__(self):
        self._close()

    def _close(self):
        # self.dev.close()
        pass

    def _open(self):
        # TODO: check return codes
        rc = self.dev.ftdi_fn.ftdi_usb_reset()
        rc |= self.dev.ftdi_fn.ftdi_usb_purge_buffers()
        rc |= self.dev.ftdi_fn.ftdi_set_bitmode(0xFF, BITMODE_MPSEE)
        rc |= self.dev.ftdi_fn.ftdi_set_latency_timer(1)

        if rc != 0:
            print("rc", rc)
        self._write([MC_TCK_D5])
        self._write([MC_SET_CLK_DIV, 119, 0x00])
        # self._write([MC_SET_CLK_DIV, 0x00, 0x00])

        self._write([MC_SETB_LOW, 0x10, 0x13])

    def _write(self, data):
        if 1:
            buf = create_string_buffer(bytes(data))
            buf_len = len(data)
            rc = self.dev.ftdi_fn.ftdi_write_data(byref(buf), buf_len)
        else:
            arr = array.array("B", data)
            buf_addr, buf_len = arr.buffer_info()
            print(data, buf_addr, buf_len)
            rc = self.dev.ftdi_fn.ftdi_write_data(buf_addr, buf_len)

        if rc < buf_len:
            print("write {} , expected {}".format(rc, buf_len), file=sys.stderr)

        return rc

    def _test(self):
        vv = [0x10, 0x80]
        for ii in range(10):
            for jj in vv:
                self._write([MC_SETB_LOW, jj, 0x93])
                time.sleep(0.2)

    def _read(self, num):
        if 1:
            buf = create_string_buffer(num)
            rc = self.dev.ftdi_fn.ftdi_read_data(byref(buf), num)
            arr = buf.raw[:rc]
        else:
            arr = array.array("B", num * [0])
            buf_addr, buf_len = arr.buffer_info()
            rc = self.dev.ftdi_fn.ftdi_read_data(buf_addr, buf_len)

        if rc < 0:
            print("read {} , expected {}".format(rc, num), file=sys.stderr)
            return []

        return arr[:rc]

    def transfer(self, data):
        self._write([MC_SETB_LOW, 0x00, 0x13])

        nb = len(data)
        setup = [
            MC_DATA_IN | MC_DATA_OUT | MC_DATA_OCN,
            (nb - 1) & 0xFF,
            ((nb - 1) >> 8) & 0xFF,
        ]

        self._write(setup)
        self._write(data)

        res = []
        its = 0
        while len(res) < nb and its < 100:
            res += self._read(nb)
            its += 1

        self._write([MC_SETB_LOW, 0x10, 0x13])

        return res


class spi_fx2(spi_interface):
    def __init__(self, speed, mode):
        pass

    def transer(self, data):
        if not isinstance(data, [bytes]):
            raise SpiException("expected bytes type for data")

    def close(self):
        pass
