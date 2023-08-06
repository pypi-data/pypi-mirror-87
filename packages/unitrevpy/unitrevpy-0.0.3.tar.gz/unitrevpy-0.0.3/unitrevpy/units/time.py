# Time units
import numpy as np
from .unit import Unit

class Time(Unit):
    """
    units used
    second, minute, hour, day, week, month, year
    """
    def __init__(self, value, *args):
        super(Time, self).__init__(value)
        if args:
            self.__convert_value_to_second = args[0]
            self.__convert_value_to_minute = args[1]
            self.__convert_value_to_hour = args[2]
            self.__convert_value_to_day = args[3]
            self.__convert_value_to_week = args[4]
            self.__convert_value_to_month = args[5]
            self.__convert_value_to_year = args[6]

    def __operator(self, convert_value):
        if isinstance(self.value, list):
            self.value = np.array(self.value)
            return list(self.value*convert_value)
        return self.value*convert_value

    def to_second(self):
        return self.__operator(self.__convert_value_to_second)

    def to_minute(self):
        return self.__operator(self.__convert_value_to_minute)

    def to_hour(self):
        return self.__operator(self.__convert_value_to_hour)

    def to_day(self):
        return self.__operator(self.__convert_value_to_day)

    def to_week(self):
        return self.__operator(self.__convert_value_to_week)

    def to_month(self):
        return self.__operator(self.__convert_value_to_month)

    def to_year(self):
        return self.__operator(self.__convert_value_to_year)


class Second(Time):
    def __init__(self, value):
        super(Second, self).__init__(value,
                                     1.0, 0.0166666667, 0.0002777778, 0.0000115741, 0.0000016534, 3.802570537E-7,
                                     3.168808781E-8)

class Minute(Time):
    def __init__(self, value):
        super(Minute, self).__init__(value,
                                     60.0, 1.0, 0.0166666667, 0.0006944444, 0.0000992063, 0.0000228154, 0.0000019013)

class Hour(Time):
    def __init__(self, value):
        super(Hour, self).__init__(value,
                                   3600.0, 60.0, 1.0, 0.0416666667, 0.005952381, 0.0013689254, 0.0001140771)

class Day(Time):
    def __init__(self, value):
        super(Day, self).__init__(value,
                                  86400.0, 1440.0, 24.0, 1.0, 0.1428571429, 0.0328542094, 0.0027378508)

class Week(Time):
    def __init__(self, value):
        super(Week, self).__init__(value,
                                   604800.0, 10080.0, 168.0, 7.0, 1.0, 0.2299794661, 0.0191649555)

class Month(Time):
    def __init__(self, value):
        super(Month, self).__init__(value,
                                    2629800.0, 43830.0, 730.5, 30.4375, 4.3482142857, 1.0, 0.0833333333)

class Year(Time):
    def __init__(self, value):
        super(Year, self).__init__(value,
                                   31557600.0, 525960.0, 8766.0, 365.25, 52.178571429, 12.0, 1.0)