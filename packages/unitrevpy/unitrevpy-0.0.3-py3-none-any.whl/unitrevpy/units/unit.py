# This is principal class or mother class
import numpy as np

class Unit:

    def __init__(self, value):
        if isinstance(value, (int, float)):
            self.value = float(value)
        elif isinstance(value, (list, tuple, set)):
            self.value = list(np.array(list(value))*1.0)
        else:
            raise TypeError("Incorrect type")

    def __str__(self):
        return str(self.value)


