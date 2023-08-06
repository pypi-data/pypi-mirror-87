import datetime
import math

from raspcuterie.devices.input.am2302 import AM2302
from raspcuterie.utils import time_based_sinus


class SinusInput(AM2302):
    type = "sinus"
    radial = math.pi / 180

    def read(self):

        humidity = time_based_sinus(datetime.datetime.now().minute, 60, 100)

        x = datetime.datetime.now() + datetime.timedelta(minutes=30)

        temperature = time_based_sinus(x.minute, 5, 25)

        return humidity, temperature

    def raw(self):
        return self.read()
