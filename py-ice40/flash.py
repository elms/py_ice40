import sys


class flash(object):
    WSR1 = 0x01
    PP = 0x02
    RD = 0x03
    RSR1 = 0x05
    WE = 0x06

    JEDICID = 0x9F

    RPD = 0xAB
    PD = 0xB9
    CE = 0xC7
    BE64 = 0xD8

    def __init__(self, spidev):
        self.spidev = spidev

    def __enter__(self):
        return self

    def __exit__(self, dtype, value, traceback):
        self.spidev.close()

    def _log(self, msg, *args, **kwargs):
        print(msg, *args, **kwargs, file=sys.stderr)
        sys.stderr.flush()

    def get24bitaddr(self, addr):
        return [(addr >> 16) & 0xFF, (addr >> 8) & 0xFF, addr & 0xFF]

    def reset(self):
        return self.spidev.transfer([0xFF, 0xFF])

    def power_up(self):
        return self.spidev.transfer([self.RPD])

    def power_down(self):
        return self.spidev.transfer([self.PD])

    def read_status(self):
        res = self.spidev.transfer([self.RSR1, 0x00])
        return res[1]

    def bulk_erase(self):
        return self.spidev.transfer([self.CE])

    def erase_64k(self, addr):
        addr24 = self.get24bitaddr(addr)
        return self.spidev.transfer([self.BE64] + addr24)

    def write_enable(self):
        return self.spidev.transfer([self.WE])

    def prog(self, addr, data):
        addr24 = self.get24bitaddr(addr)
        self._log("prog {:X} {} {}".format(addr, addr24, data))
        return self.spidev.transfer([self.PP] + addr24 + data)

    def disable_protection(self):
        self.spidev.transfer([self.WSR1, 0x00])
        stat = self.wait()
        if stat != 0:
            raise Exception("protection not disabled: status {:X}".format(stat))

    def wait(self):
        count = 0
        while 1:
            stat = self.read_status()
            if stat & 0x01 == 0:
                if count < 2:
                    self._log("r", end="")
                    count += 1
                else:
                    self._log("R")
                    break
            else:
                self._log(".", end="")
                count = 0
        return stat

    def jedic_id(self, num=5):
        res = self.spidev.transfer([self.JEDICID] + num * [0x00])
        return res[1:]

    def read(self, addr, num):
        addr24 = self.get24bitaddr(addr)
        self._log("reading at {:X} {}".format(addr, addr24))
        res = self.spidev.transfer([self.RD] + addr24 + num * [0])
        return res[4:]


def main():
    from periphery import GPIO, SPI

    # TODO: hack for testing
    GPIO(17, "out").write(False)
    GPIO(27, "out").write(False)

    with flash(SPI("/dev/spidev0.0", 3, 1e6)) as f:
        print(f.reset())
        print(f.power_up())
        print("status", f.read_status())
        print("jedic", f.jedic_id())
        print(f.read(0, 100))
        print(f.power_down())

        print("status", f.read_status())

        print("read_write_read")
        print(f.reset())
        print(f.power_up())
        print("status", f.read_status())
        f.disable_protection()
        f.write_enable()
        print("status", f.read_status())

        addr = 256 << 10
        print("read pre", f.read(addr, 100))
        f.erase_64k(addr)
        f.wait()
        print("read mid", f.read(addr, 100))
        f.write_enable()
        f.prog(addr, [xx for xx in range(100)])
        print("status", f.read_status())
        f.wait()
        print("status", f.read_status())

        print("read post", f.read(addr, 100))
        print(f.power_down())


if __name__ == "__main__":
    main()
