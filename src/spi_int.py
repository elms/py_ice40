class SpiNotImplemented(exception):
    pass

class spi_interface():
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

import libftdi

class spi_ftdi(spi_interface):
    def __init__(self, speed, mode, interface='A', **kwargs):
        pass


class spi_fx2(spi_interface):
    def __init__(self, speed, mode):
        pass

    def transer(self, data):
        if not isinstance(data, [bytes]):
            raise SpiException('expected bytes type for data')

    def close(self):
        pass
    
        

