import spi_int
import time

aa = spi_int.spi_ftdi(1e5, 3)

#aa._test()

cnt = 0x80
data = [xx%256 for xx in range(cnt)]
res = aa.transfer(data)
print(res)

#time.sleep(1)
#aa._test()
