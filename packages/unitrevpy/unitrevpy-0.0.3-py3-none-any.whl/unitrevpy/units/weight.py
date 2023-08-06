# Weight units
import numpy as np
from .unit import Unit

class Weight(Unit):
    """
    units used
    kilogram, gram, millimeter, metric ton, long ton, short ton, pound, ounce, carat, atomic mass unit
    """
    def __init__(self, value, *args):
        super(Weight, self).__init__(value)
        if args:
            self.__convert_value_to_kilogram = args[0]
            self.__convert_value_to_gram = args[1]
            self.__convert_value_to_milligram = args[2]
            self.__convert_value_to_metric_ton = args[3]
            self.__convert_value_to_long_ton = args[4]
            self.__convert_value_to_short_ton = args[5]
            self.__convert_value_to_pound = args[6]
            self.__convert_value_to_ounce = args[7]
            self.__convert_value_to_carat = args[8]
            self.__convert_value_to_atomic_mass_unit = args[9]

    def __operator(self, convert_value):
        if isinstance(self.value, list):
            self.value = np.array(self.value)
            return list(self.value*convert_value)
        return self.value*convert_value

    def to_kilogram(self):
        return self.__operator(self.__convert_value_to_kilogram)

    def to_gram(self):
        return self.__operator(self.__convert_value_to_gram)

    def to_milligram(self):
        return self.__operator(self.__convert_value_to_milligram)

    def to_metric_ton(self):
        return self.__operator(self.__convert_value_to_metric_ton)

    def to_long_ton(self):
        return self.__operator(self.__convert_value_to_long_ton)

    def to_short_ton(self):
        return self.__operator(self.__convert_value_to_short_ton)

    def to_pound(self):
        return self.__operator(self.__convert_value_to_pound)

    def to_ounce(self):
        return self.__operator(self.__convert_value_to_ounce)

    def to_carat(self):
        return self.__operator(self.__convert_value_to_carat)

    def to_atomic_mass_unit(self):
        return self.__operator(self.__convert_value_to_atomic_mass_unit)


class Kilogram(Weight):

    def __init__(self, value):
        super(Kilogram, self).__init__(value,
                                       1.0, 1000.0, 1000000.0, 0.001, 0.0009842073, 0.0011023122, 2.2046244202,
                                       35.273990723, 5000.0, 6.022136652E+26)

class Gram(Weight):

    def __init__(self, value):
        super(Gram, self).__init__(value,
                                   0.001, 1.0, 1000.0, 0.000001, 9.842073304E-7, 0.0000011023, 0.0022046244,
                                   0.0352739907, 5.0, 6.022136652E+23)

class Milligram(Weight):

    def __init__(self, value):
        super(Milligram, self).__init__(value,
                                        0.000001, 0.001, 1.0, 9.999999999E-10, 9.842073304E-10, 1.10231221E-9,
                                        0.0000022046, 0.000035274, 0.005, 602213665200000000000.0)

class MetricTon(Weight):

    def __init__(self, value):
        super(MetricTon, self).__init__(value,
                                        1000.0, 1000000.0, 1000000000.0, 1.0, 0.9842073304, 1.1023122101,
                                        2204.6244202, 35273.990723, 5000000.0, 6.022136652E+29)

class LongTon(Weight):

    def __init__(self, value):
        super(LongTon, self).__init__(value,
                                      1016.04608, 1016046.08, 1016046080, 1.01604608, 1.0, 1.12, 2240.0, 35840,
                                      5080230.4, 6.118768338E+29)

class ShortTon(Weight):

    def __init__(self, value):
        super(ShortTon, self).__init__(value,
                                       907.184, 907184.0, 907184000.0, 0.907184, 0.8928571429, 1.0, 2000.0,
                                       32000.0, 4535920.0, 5.463186016E+29)

class Pound(Weight):

    def __init__(self, value):
        super(Pound, self).__init__(value,
                                    0.453592, 453.592, 453592.0, 0.000453592, 0.0004464286, 0.0005,
                                    1.0, 16.0, 2267.96, 2.731593008E+26)

class Ounce(Weight):

    def __init__(self, value):
        super(Ounce, self).__init__(value,
                                    0.0283495, 28.3495, 28349.5, 0.0000283495, 0.0000279018, 0.00003125,
                                    0.0625, 1.0, 141.7475, 1.70724563E+25)

class Carat(Weight):

    def __init__(self, value):
        super(Carat, self).__init__(value,
                                    0.0002, 0.2, 200.0, 2.E-7, 1.96841466E-7, 2.20462442E-7, 0.0004409249,
                                    0.0070547981, 1.0, 1.20442733E+23)

class AtomicMassUnit(Weight):
    
    def __init__(self, value):
        super(AtomicMassUnit, self).__init__(value,
                                             1.660540199E-27, 1.660540199E-24, 1.660540199E-21, 1.660540199E-30,
                                             1.634315837E-30, 1.830433737E-30, 3.660867475E-27, 5.85738796E-26,
                                             8.302700999E-24, 1.0)