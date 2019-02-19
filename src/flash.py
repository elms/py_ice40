from periphery import GPIO, SPI

class flash(object):
    MODE = 3
    
    def __init__(self, spidev_path='/dev/spidev0.0', speed=1e5):
        self.spidev = SPI(spidev_path, self.MODE, speed)

    def __enter__(self):
        return self

    def __exit__(self, dtype, value, traceback):
        self.spidev.close()

    def reset(self):
        return self.spidev.transfer([0xff, 0xff])
    
    def jedec_id(self):
        data = bytes([0x9f] + 50*[0x00])
        print(data)
        res = self.spidev.transfer(data)
        print(len(res))
        return res


def main():
    with flash() as f:
        print(f.reset())
        print(f.jedec_id())

if __name__ == '__main__':
    main()
