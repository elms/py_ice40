from periphery import GPIO, SPI
import time

class config(object):

  DONE_ITS = 100

  def __init__(self, ss_pin=8, cdone_pin=4, creset_pin=17, speed=1e6,
               spidev_path='/dev/spidev0.0',**kwargs):
    self.ss = GPIO(ss_pin, 'out')
    self.cdone = GPIO(cdone_pin, 'in')
    self.creset = GPIO(creset_pin, 'out')

    # mode
    mode = 2
    self.spidev = SPI(spidev_path, mode, speed, extra_flags=0x40)

  def set_ss(self, val):
    self.ss.write(val)

  def reset(self, val):
    if val:
      self.creset.write(False)
    else:
      self.creset.write(True)

  def wait_done(self):
    done = 0
    cnt = 0
    while done==0 and cnt < self.DONE_ITS:
      time.sleep(100e-3)
      done = self.cdone.read()
      cnt += 1

  """
  def xfer(self, data):
    import fcntl
    import array
    import periphery
    
    try:
      buf = array.array('B', data)
    except OverflowError:
      raise ValueError("Invalid data bytes.")
    
    buf_addr, buf_len = buf.buffer_info()

    # Prepare transfer structure
    spi_xfer = periphery.spi._CSpiIocTransfer()
    spi_xfer.tx_buf = buf_addr
    spi_xfer.rx_buf = buf_addr
    spi_xfer.len = buf_len
    spi_xfer.cs_change = 0

    # Transfer
    try:
      fcntl.ioctl(self.spidev._fd, periphery.spi.SPI._SPI_IOC_MESSAGE_1, spi_xfer)
    except OSError as e:
      raise periphery.spi.SPIError(e.errno, "SPI transfer: " + e.strerror)
  """    
      
  def sram_config(self, image):

    self.reset(True)
    time.sleep(10e-3)
    self.set_ss(False)
    time.sleep(10e-3)
    self.reset(False)
    time.sleep(10e-3)

    CHUNK = 1024
    for i in range(len(image)//CHUNK + 1):
      self.spidev.transfer(image[i*CHUNK:(i+1)*CHUNK])
      # self.xfer(image[i*CHUNK:(i+1)*CHUNK])

    # extra 49 bits
    self.spidev.transfer(7*[0,])

          
def main(fname):
  cfg = config()
  with open(fname, 'rb') as f:
    image = f.read()
  cfg.sram_config(image)


if __name__ == '__main__':
  import sys
  main(sys.argv[1])
