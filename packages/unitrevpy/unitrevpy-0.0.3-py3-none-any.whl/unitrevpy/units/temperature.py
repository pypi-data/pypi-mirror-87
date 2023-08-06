# Temperature units
import numpy as np
from .unit import Unit

class Temperature(Unit):
    """
    units used
    celsius, kelvin, fahrenheit
    """
    def __init__(self, value):
        super(Temperature, self).__init__(value)


class Celsius(Temperature):

    def to_celsius(self):
        return self.value

    def to_kelvin(self):
        if isinstance(self.value, list):
            self.value = np.array(self.value)
            return list(self.value + 273.15)
        return self.value + 273.15

    def to_fahrenheit(self):
        if isinstance(self.value, list):
            self.value = np.array(self.value)
            return list(self.value * (9/5) + 32)
        return self.value * (9/5) + 32


class Kelvin(Temperature):

    def to_celsius(self):
        if isinstance(self.value, list):
            self.value = np.array(self.value)
            return list(self.value - 273)
        return self.value - 273.15

    def to_kelvin(self):
        return self.value

    def to_fahrenheit(self):
        if isinstance(self. value, list):
            self.value = np.array(self.value)
            return list((self.value - 273.15)*(9/5) + 32)
        return (self.value - 273.15)*(9/5) + 32


class Fahrenheit(Temperature):

    def to_celsius(self):
        if isinstance(self.value, list):
            self.value = np.array(self.value)
            return list((self.value - 32)*(5/9))
        return (self.value - 32)*(5/9)

    def to_kelvin(self):
        if isinstance(self.value, list):
            self.value = np.array(self.value)
            return list((self.value - 32) * (5 / 9) + 273.15)
        return (self.value - 32)*(5/9) + 273.15

    def to_fahrenheit(self):
        return self.value
