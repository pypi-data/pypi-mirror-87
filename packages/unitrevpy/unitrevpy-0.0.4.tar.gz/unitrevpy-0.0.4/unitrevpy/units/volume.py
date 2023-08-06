# Volume units
import numpy as np
from .unit import Unit

class Volume(Unit):

    """
    units used
    cubic_mete, cubic_kilometer, cubic_centimeter, cubic_millimeter, liter, milliliter, us_gallon, us_quart,
    us_pint, us_cup, us_fluid_ounce, us_table_spoon, us_tea_spoon, imperial_gallon, imperial_quart, imperial_pint,
    imperial_fluid_ounce, imperial_table_spoon, imperial_tea_spoon, cubic_mile, cubic_yard,
    cubic_foot, cubic_inch
    """
    def __init__(self, value, *args):
        super(Volume, self).__init__(value)
        if args:
            self.__convert_value_to_cubic_meter = args[0]
            self.__convert_value_to_cubic_kilometer = args[1]
            self.__convert_value_to_cubic_centimeter = args[2]
            self.__convert_value_to_cubic_millimeter = args[3]
            self.__convert_value_to_liter = args[4]
            self.__convert_value_to_milliliter = args[5]
            self.__convert_value_to_us_gallon = args[6]
            self.__convert_value_to_us_quart = args[7]
            self.__convert_value_to_us_pint = args[8]
            self.__convert_value_to_us_cup = args[9]
            self.__convert_value_to_us_fluid_ounce = args[10]
            self.__convert_value_to_us_table_spoon = args[11]
            self.__convert_value_to_us_tea_spoon = args[12]
            self.__convert_value_to_imperial_gallon = args[13]
            self.__convert_value_to_imperial_pint = args[14]
            self.__convert_value_to_imperial_quart = args[15]
            self.__convert_value_to_imperial_fluid_ounce = args[16]
            self.__convert_value_to_imperial_table_spoon = args[17]
            self.__convert_value_to_imperial_tea_spoon = args[18]
            self.__convert_value_to_cubic_mile = args[19]
            self.__convert_value_to_cubic_yard = args[20]
            self.__convert_value_to_cubic_foot = args[21]
            self.__convert_value_to_cubic_inch = args[22]

    def __operator(self, convert_value):
        if isinstance(self.value, list):
            self.value = np.array(self.value)
            return list(self.value * convert_value)
        return self.value*convert_value

    def to_cubic_meter(self):
        return self.__operator(self.__convert_value_to_cubic_meter)

    def to_kilometer(self):
        return self.__operator(self.__convert_value_to_cubic_kilometer)

    def to_cubic_centimeter(self):
        return self.__operator(self.__convert_value_to_cubic_centimeter)

    def to_cubic_millimeter(self):
        return self.__operator(self.__convert_value_to_cubic_millimeter)

    def to_liter(self):
        return self.__operator(self.__convert_value_to_liter)

    def to_milliliter(self):
        return self.__operator(self.__convert_value_to_milliliter)

    def to_us_gallon(self):
        return self.__operator(self.__convert_value_to_us_gallon)

    def to_us_quart(self):
        return self.__operator(self.__convert_value_to_us_quart)

    def to_us_pint(self):
        return self.__operator(self.__convert_value_to_us_pint)

    def to_us_cup(self):
        return self.__operator(self.__convert_value_to_us_cup)

    def to_us_fluid_ounce(self):
        return self.__operator(self.__convert_value_to_us_fluid_ounce)

    def to_us_table_spoon(self):
        return self.__operator(self.__convert_value_to_us_table_spoon)

    def to_us_tea_spoon(self):
        return self.__operator(self.__convert_value_to_us_tea_spoon)

    def to_imperial_gallon(self):
        return self.__operator(self.__convert_value_to_imperial_gallon)

    def to_imperial_quart(self):
        return self.__operator(self.__convert_value_to_imperial_quart)

    def to_imperial_pint(self):
        return self.__operator(self.__convert_value_to_imperial_pint)

    def to_imperial_fluid_ounce(self):
        return self.__operator(self.__convert_value_to_imperial_fluid_ounce)

    def to_imperial_table_spoon(self):
        return self.__operator(self.__convert_value_to_imperial_table_spoon)

    def to_imperial_tea_spoon(self):
        return self.__operator(self.__convert_value_to_imperial_tea_spoon)

    def to_cubic_mile(self):
        return self.__operator(self.__convert_value_to_cubic_mile)

    def to_cubic_yard(self):
        return self.__operator(self.__convert_value_to_cubic_yard)

    def to_cubic_foot(self):
        return self.__operator(self.__convert_value_to_cubic_foot)

    def to_cubic_inch(self):
        return self.__operator(self.__convert_value_to_cubic_inch)


class CubicMeter(Volume):

    def __init__(self, value):
        super(CubicMeter, self).__init__(value,
                                         1.0, 1.E-9, 1000000.0, 1000000000.0, 1000.0, 1000000.0,
                                         264.17217686, 1056.6887074, 2113.3774149, 4226.7548297,
                                         33814.038638, 67628.077276, 202884.23183, 219.9692483,
                                         879.8769932, 1759.7539864, 35195.079728, 56312.127565,
                                         168936.38269, 2.399128636E-10, 1.3079506193, 35.314666721,
                                         61023.744095)

class CubicKilometer(Volume):

    def __init__(self, value):
        super(CubicKilometer, self).__init__(value,
                                             1000000000.0, 1.0, 1000000000000000.0, 1000000000000000000.0,
                                             1000000000000.0, 1000000000000000.0, 264172176858.0, 1056688707432.0,
                                             2113377414864.0, 4226754829728.0, 33814038637823.0, 67628077275645.0,
                                             202884231826936.0, 219969248299.0, 879876993196.0, 1759753986393.0,
                                             35195079727854.0, 56312127564566.0, 168936382693699.0, 0.2399128636,
                                             1307950619.3, 35314666721.0, 61023744094732.0)


class CubicCentimeter(Volume):

    def __init__(self, value):
        super(CubicCentimeter, self).__init__(value,
                                              0.000001, 9.999999999E-16, 1.0, 1000.0, 0.001, 1.0, 0.0002641722,
                                              0.0010566887, 0.0021133774, 0.0042267548, 0.0338140386, 0.0676280773,
                                              0.2028842318, 0.0002199692, 0.000879877, 0.001759754, 0.0351950797,
                                              0.0563121276, 0.1689363827, 2.399128636E-16, 0.000001308, 0.0000353147,
                                              0.0610237441)

class CubicMillimeter(Volume):

    def __init__(self, value):
        super(CubicMillimeter, self).__init__(value,
                                              1.E-9, 1.E-18, 0.001, 1.0, 0.000001, 0.001, 2.641721768E-7, 0.0000010567,
                                              0.0000021134, 0.0000042268, 0.000033814, 0.0000676281, 0.0002028842,
                                              2.199692482E-7, 8.798769931E-7, 0.0000017598, 0.0000351951, 0.0000563121,
                                              0.0001689364, 2.399128636E-19, 1.307950619E-9, 3.531466672E-8,
                                              3.531466672E-8)


class Liter(Volume):

    def __init__(self, value):
        super(Liter, self).__init__(value,
                                    0.001, 1.E-12, 1000, 1000000, 1.0, 1000.0, 0.2641721769, 1.0566887074, 2.1133774149,
                                    4.2267548297, 33.814038638, 67.628077276, 202.88423183, 0.2199692483, 0.8798769932,
                                    1.7597539864, 35.195079728, 56.312127565, 168.93638269, 2.399128636E-13,
                                    0.0013079506, 0.0353146667, 61.023744095)

class Milliliter(Volume):

    def __init__(self, value):
        super(Milliliter, self).__init__(value,
                                         0.000001, 9.999999999E-16, 1.0, 1000.0, 0.001, 1.0, 0.0002641722, 0.0010566887,
                                         0.0021133774, 0.0042267548, 0.0338140386, 0.0676280773, 0.2028842318,
                                         0.0002199692, 0.000879877, 0.001759754, 0.0351950797, 0.0563121276,
                                         0.1689363827, 2.399128636E-16, 0.000001308, 0.0000353147, 0.0610237441)

class USGallon(Volume):

    def __init__(self, value):
        super(USGallon, self).__init__(value,
                                       0.00378541, 3.78541E-12, 3785.41, 3785410.0, 3.78541, 3785.41, 1.0, 4.0, 8.0,
                                       16.0, 128.0, 256.0, 768.0, 0.8326737922, 3.3306951688, 6.6613903376,
                                       133.22780675, 213.1644908, 639.49347241, 9.081685531E-13,
                                       0.0049511294, 0.1336804926, 230.99989113)

class USQuart(Volume):

    def __init__(self, value):
        super(USQuart, self).__init__(value,
                                      0.0009463525, 9.463525E-13, 946.3525, 946352.5, 0.9463525, 946.3525, 0.25, 1.0,
                                      2.0, 4.0, 32.0, 64.0, 192.0, 0.2081684481, 0.8326737922, 1.6653475844,
                                      33.306951688, 53.291122701, 159.8733681, 2.270421382E-13, 0.0012377823,
                                      0.0334201231, 57.749972783)

class USPint(Volume):

    def __init__(self, value):
        super(USPint, self).__init__(value,
                                     0.0004731763, 4.7317625E-13, 473.17625, 473176.25, 0.47317625, 473.17625,
                                     0.125, 0.5, 1.0, 2.0, 16.0, 32.0, 96.0, 0.104084224, 0.4163368961,
                                     0.8326737922, 16.653475844, 26.645561351, 79.936684052, 1.135210691E-13,
                                     0.0006188912, 0.0167100616, 28.874986392)


class USCup(Volume):

    def __init__(self, value):
        super(USCup, self).__init__(value,
                                    0.0002365881, 2.36588125E-13, 236.588125, 236588.125, 0.236588125, 236.588125,
                                    0.0625, 0.25, 0.5, 1.0, 8.0, 16.0, 48.0, 0.052042112, 0.2081684481, 0.4163368961,
                                    8.326737922, 13.322780675, 39.968342026, 5.676053457E-14, 0.0003094456,
                                    0.0083550308, 14.437493196)

class USFluidOunce(Volume):

    def __init__(self, value):
        super(USFluidOunce, self).__init__(value,
                                           0.0000295735, 2.957351562E-14, 29.573515625, 29573.515625, 0.0295735156,
                                           29.573515625, 0.0078125, 0.03125, 0.0625, 0.125, 1.0, 2.0, 6.0,
                                           0.006505264, 0.026021056, 0.052042112, 1.0408422403, 1.6653475844,
                                           4.9960427532, 7.095066821E-15, 0.0000386807, 0.0010443788, 1.8046866495)


class USTableSpoon(Volume):

    def __init__(self, value):
        super(USTableSpoon, self).__init__(value,
                                           0.0000147868, 1.478675781E-14, 14.786757812, 14786.757812, 0.0147867578,
                                           14.786757812, 0.00390625, 0.015625, 0.03125, 0.0625, 0.5, 1.0, 3.0,
                                           0.003252632, 0.013010528, 0.026021056, 0.5204211201, 0.8326737922,
                                           2.4980213766, 3.54753341E-15, 0.0000193403, 0.0005221894, 0.9023433247)

class USTeaSpoon(Volume):

    def __init__(self, value):
        super(USTeaSpoon, self).__init__(value,
                                         0.0000049289, 4.92891927E-15, 4.9289192708, 4928.9192708, 0.0049289193,
                                         4.9289192708, 0.0013020833, 0.0052083333, 0.0104166667, 0.0208333333,
                                         0.1666666667, 0.3333333333, 1.0, 0.0010842107, 0.0043368427, 0.0086736853,
                                         0.1734737067, 0.2775579307, 0.8326737922, 1.182511136E-15, 0.0000064468,
                                         0.0001740631, 0.3007811082)

class ImperialGallon(Volume):

    def __init__(self, value):
        super(ImperialGallon, self).__init__(value,
                                             0.00454609, 4.54609E-12, 4546.09, 4546090.0, 4.54609, 4546.09,
                                             1.2009504915, 4.803801966, 9.6076039319, 19.215207864, 153.72166291,
                                             307.44332582, 922.32997747, 1.0, 4.0, 8.0, 160.0, 256.0, 768.0,
                                             1.09066547E-12, 0.0059460612, 0.1605436532, 277.41943279)

class ImperialQuart(Volume):

    def __init__(self, value):
        super(ImperialQuart, self).__init__(value,
                                            0.0011365225, 1.1365225E-12, 1136.5225, 1136522.5, 1.1365225, 1136.5225,
                                            0.3002376229, 1.2009504915, 2.401900983, 4.803801966, 38.430415728,
                                            76.860831456, 230.58249437, 0.25, 1.0, 2.0, 40.0, 64.0, 192.0,
                                            2.726663675E-13, 0.0014865153, 0.0401359133, 69.354858198)

class ImperialPint(Volume):

    def __init__(self, value):
        super(ImperialPint, self).__init__(value,
                                           0.0005682613, 5.6826125E-13, 568.26125, 568261.25, 0.56826125, 568.26125,
                                           0.1501188114, 0.6004752457, 1.2009504915, 2.401900983, 19.215207864,
                                           38.430415728, 115.29124718, 0.125, 0.5, 1.0, 20.0, 32.0, 96.0,
                                           1.363331837E-13, 0.0007432577, 0.0200679567, 34.677429099)


class ImperialFluidOunce(Volume):

    def __init__(self, value):
        super(ImperialFluidOunce, self).__init__(value,
                                                 0.0000284131, 2.84130625E-14, 28.4130625, 28413.0625, 0.0284130625,
                                                 28.4130625, 0.0075059406, 0.0300237623, 0.0600475246, 0.1200950491,
                                                 0.9607603932, 1.9215207864, 5.7645623592, 0.00625, 0.025, 0.05,
                                                 1.0, 1.6, 4.8, 6.816659189E-15, 0.0000371629, 0.0010033978,
                                                 1.7338714549)


class ImperialTableSpoon(Volume):

    def __init__(self, value):
        super(ImperialTableSpoon, self).__init__(value,
                                                 0.0000177582, 1.775816406E-14, 17.758164063, 17758.164063,
                                                 0.0177581641, 17.758164063, 0.0046912129, 0.0187648514, 0.0375297029,
                                                 0.0750594057, 0.6004752457, 1.2009504915, 3.6028514745,
                                                 0.00390625, 0.015625, 0.03125, 0.625, 1.0, 3.0, 4.260411993E-15,
                                                 0.0000232268, 0.0006271236, 1.0836696593)


class ImperialTeaSpoon(Volume):

    def __init__(self, value):
        super(ImperialTeaSpoon, self).__init__(value,
                                               0.0000059194, 5.91938802E-15, 5.9193880208, 5919.3880208, 0.005919388,
                                               5.9193880208, 0.0015637376, 0.0062549505, 0.012509901, 0.0250198019,
                                               0.2001584152, 0.4003168305, 1.2009504915, 0.0013020833, 0.0052083333,
                                               0.0104166667, 0.2083333333, 0.3333333333, 1.0, 1.420137331E-15,
                                               0.0000077423, 0.0002090412, 0.3612232198)


class CubicMile(Volume):

    def __init__(self, value):
        super(CubicMile, self).__init__(value,
                                        4168180000.0, 4.16818, 4168180000000000.0, 4168179999999999500.0,
                                        4168180000000.0, 4168180000000000.0, 1101117184136.0, 4404468736544.0,
                                        8808937473087.0, 17617874946175.0, 140942999569399.0, 281885999138799.0,
                                        845657997416396.0, 916871421375.0, 3667485685501.0, 7334971371002.0,
                                        146699427420047.0, 234719083872075.0, 704157251616224.0, 1.0,
                                        5451773612.4, 147197887535.0, 254357949660781.0)

class CubicYard(Volume):

    def __init__(self, value):
        super(CubicYard, self).__init__(value,
                                        0.764554858, 7.645548579E-10, 764554.85798, 764554857.98, 764.55485798,
                                        764554.85798, 201.97412116, 807.89648464, 1615.7929693, 3231.5859386,
                                        25852.687509, 51705.375017, 155116.12505, 168.17855739, 672.71422958,
                                        1345.4284592, 26908.569183, 43053.710693, 129161.13208, 1.834265453E-10,
                                        1.0, 27.0, 46656.0)

class CubicFoot(Volume):

    def __init__(self, value):
        super(CubicFoot, self).__init__(value,
                                        0.0283168466, 2.831684659E-11, 28316.846592, 28316846.592, 28.316846592,
                                        28316.846592, 7.480523006, 29.922092024, 59.844184048, 119.6883681,
                                        957.50694476, 1915.0138895, 5745.0416686, 6.228835459, 24.915341836,
                                        49.830683672, 996.61367345, 1594.5818775, 4783.7456325, 6.793575755E-12,
                                        0.037037037, 1.0, 1728.0)

class CubicInch(Volume):

    def __init__(self, value):
        super(CubicInch, self).__init__(value,
                                        0.0000163871, 1.6387064E-14, 16.387064, 16387.064, 0.016387064, 16.387064,
                                        0.0043290064, 0.0173160255, 0.034632051, 0.0692641019, 0.5541128153,
                                        1.1082256305, 3.3246768915, 0.0036046501, 0.0144186006, 0.0288372012,
                                        0.576744024, 0.9227904384, 2.7683713151, 3.931467451E-15, 0.0000214335,
                                        0.0005787037, 1.0)
