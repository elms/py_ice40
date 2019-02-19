import config
from periphery import GPIO

class example1(config.config):
    def __init__(self, ss_pin=8, cdone_pin=4, creset_pin=17, speed=1e6,
               spidev_path='/dev/spidev0.0'):
        super().__init__(ss_pin, cdone_pin, creset_pin, speed, spidev_path)
        
        # set SPI switch for FPGA to be SPI slave
        self.flash_switch = GPIO(5, 'out')
        self.flash_switch.write(False)

        # HACK: reset FPGA 2
        self.flash_switch = GPIO(27, 'out')
        self.flash_switch.write(False)

        
class example2(config.config):
    # TODO: ss_pin should be 7 for rework
    def __init__(self, ss_pin=1, cdone_pin=22, creset_pin=27, speed=1e6,
               spidev_path='/dev/spidev0.1'):
        super().__init__(ss_pin, cdone_pin, creset_pin, speed, spidev_path)
        
        # HACK: reset FPGA 2
        self.flash_switch = GPIO(17, 'out')
        self.flash_switch.write(False)


def main(fname):
  cfg = example2()
  with open(fname, 'rb') as f:
    image = f.read()
  cfg.sram_config(image)

  if not cfg.wait_done():
    print("ERROR: CDONE timeout.")

if __name__ == '__main__':
  import sys
  main(sys.argv[1])
