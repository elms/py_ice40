from periphery import GPIO, SPI
import time

class config(object):

  DONE_ITS = 100
  CHUNK = 4*1024
  DELAY = 10e-3
  MODE = 3
  
  def __init__(self, ss_pin, cdone_pin, creset_pin, speed, spidev=SPI(spidev_path, self.MODE, speed)):
    self.ss = GPIO(ss_pin, 'out')
    self.cdone = GPIO(cdone_pin, 'in')
    self.creset = GPIO(creset_pin, 'out')
    self.spidev = spidev

  def sleep(self):
    time.sleep(self.DELAY)
    
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
      self.sleep()
      done = self.cdone.read()
      cnt += 1
    return done
      
  def sram_config(self, image):
    self.reset(True)
    self.sleep()

    self.set_ss(False)
    self.sleep()

    self.reset(False)
    self.sleep()

    for i in range(0, len(image), self.CHUNK):
      self.spidev.transfer(image[i:i + self.CHUNK])

    # extra 49 bits
    self.spidev.transfer(7*[0,])

def main(fname):
  cfg = config()
  with open(fname, 'rb') as f:
    image = f.read()
  cfg.sram_config(image)

  if not cfg.wait_done():
    print("ERROR: CDONE timeout.")


if __name__ == '__main__':
  import sys
  main(sys.argv[1])
