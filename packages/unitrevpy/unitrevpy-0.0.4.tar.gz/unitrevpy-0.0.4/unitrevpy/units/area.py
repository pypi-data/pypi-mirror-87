# Area units
import numpy as np
from .unit import Unit

class Area(Unit):
    """
    units used
    square_meter, hectare, square_mile, square_yard, square_foot, square_inch, acre
    """
    def __init__(self, value, *args):
        super(Area, self).__init__(value)
        if args:
            self.__value_convert_to_square_meter = args[0]
            self.__value_convert_to_hectare = args[1]
            self.__value_convert_to_square_mile = args[2]
            self.__value_convert_to_square_yard = args[3]
            self.__value_convert_to_square_foot = args[4]
            self.__value_convert_to_square_inch = args[5]
            self.__value_convert_to_acre = args[6]

    def __operator(self, convert_value):
        if isinstance(self.value, list):
            self.value = np.array(self.value)
            return list(self.value * convert_value)
        return self.value*convert_value

    def to_square_meter(self):
        return self.__operator(self.__value_convert_to_square_meter)

    def to_hectare(self):
        return self.__operator(self.__value_convert_to_hectare)

    def to_square_mile(self):
        return self.__operator(self.__value_convert_to_square_mile)

    def to_square_yard(self):
        return self.__operator(self.__value_convert_to_square_yard)

    def to_square_foot(self):
        return self.__operator(self.__value_convert_to_square_foot)

    def to_square_inch(self):
        return self.__operator(self.__value_convert_to_square_inch)

    def to_acre(self):
        return self.__operator(self.__value_convert_to_acre)


class SquareMeter(Area):

    def __init__(self, value):
        super(SquareMeter, self).__init__(value, 1.0, 0.0001, 3.861018768E-7, 1.1959900463,
                                          10.763910417, 1550.0031, 0.0002471054)

class Hectare(Area):

    def __init__(self, value):
        super(Hectare, self).__init__(value, 10000.0, 1.0, 0.0038610188, 11959.900463,
                                      107639.10417, 15500031.0, 2.4710538147)

class SquareMile(Area):

    def __init__(self, value):
        super(SquareMile, self).__init__(value, 2589990.0, 258.999, 1.0, 3097602.26,
                                         27878420.34, 4014492529.0, 640.00046695)

class SquareYard(Area):

    def __init__(self, value):
        super(SquareYard, self).__init__(value, 0.83612736, 0.0000836127, 3.228303429E-7,
                                         1.0, 9.0, 1296.0, 0.0002066116)

class SquareFoot(Area):

    def __init__(self, value):
        super(SquareFoot, self).__init__(value, 0.09290304, 0.0000092903, 3.58700381E-8,
                                         0.1111111111, 1.0, 144.0, 0.0000229568)

class SquareInch(Area):

    def __init__(self, value):
        super(SquareInch, self).__init__(value, 0.00064516, 6.4516E-8, 2.490974868E-10,
                                         0.0007716049, 0.0069444444, 1.0, 1.594225079E-7)

class Acre(Area):

    def __init__(self, value):
        super(Acre, self).__init__(value, 4046.8564224, 0.4046856422, 0.0015624989,
                                   4840.0, 43560.0, 6272640.0, 1.0)


