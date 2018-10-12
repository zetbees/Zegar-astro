from math import cos, sin, acos, asin, tan
from math import degrees as deg, radians as rad
from datetime import date, datetime, time

def int_zach(latgeo, longgeo, czas):
    # latgeo i longgeo - dł i sz geograficzna
    # obliczniea z portalu internetowego:
    s = sun(latgeo, longgeo)
    czas_zach = s.sunset()
    print('Wschod')
    # ponieważ uzyskujemy tylko godzinę zachodu konwersja przez str celem uzyskania timestamp'u
    data_obecna = datetime.now()
    czas_zach=( data_obecna.strftime('%Y-%m-%d')+' '+czas_zach.strftime('%H:%M:%S'))
    czas_zach = datetime.strptime(czas_zach, '%Y-%m-%d %H:%M:%S')
    int_czas = int((czas_zach.timestamp())/60)+czas
    return int_czas

def int_wsch(latgeo, longgeo, czas):
    # latgeo i longgeo - dł i sz geograficzna
    # obliczniea z portalu internetowego:
    s = sun(latgeo, longgeo)
    czas_zach = s.sunrise()
    # ponieważ uzyskujemy tylko godzinę zachodu konwersja przez str celem uzyskania timestamp'u
    data_obecna = datetime.now()
    czas_zach=( data_obecna.strftime('%Y-%m-%d')+' '+czas_zach.strftime('%H:%M:%S'))
    czas_zach = datetime.strptime(czas_zach, '%Y-%m-%d %H:%M:%S')
    int_czas = int((czas_zach.timestamp())/60)+czas
    return int_czas

def po_zach(latgeo, longgeo, czas=None):
    # latgeo i longgeo - dł i sz geograficzna
    # obliczniea z portalu internetowego:
    s = sun(latgeo, longgeo)
    czas_zach = s.sunset()
    # ponieważ uzyskujemy tylko godzinę zachodu konwersja przez str celem uzyskania timestamp'u
    data_obecna = datetime.now()
    czas_zach=( data_obecna.strftime('%Y-%m-%d')+' '+czas_zach.strftime('%H:%M:%S'))
    print(czas_zach, type(czas_zach))
    czas_zach = datetime.strptime(czas_zach, '%Y-%m-%d %H:%M:%S')
    czas = int((data_obecna.timestamp() - czas_zach.timestamp())/60)
    print(czas)
    return czas

def po_wsch(latgeo, longgeo, czas=None):
    s = sun(latgeo, longgeo)
    czas_zach = s.sunrise()
    # ponieważ uzyskujemy tylko godzinę zachodu konwersja przez str celem uzyskania timestamp'u
    data_obecna = datetime.now()
    czas_zach = (data_obecna.strftime('%Y-%m-%d') + ' ' + czas_zach.strftime('%H:%M:%S'))
    print(czas_zach, type(czas_zach))
    czas_zach = datetime.strptime(czas_zach, '%Y-%m-%d %H:%M:%S')
    czas = int((data_obecna.timestamp() - czas_zach.timestamp()) / 60)
    print(czas)
    return czas


class sun:
    """
    Calculate sunrise and sunset based on equations from NOAA
    http://www.srrb.noaa.gov/highlights/sunrise/calcdetails.html

    typical use, calculating the sunrise at the present day:

    import datetime
    import sunrise
    s = sun(lat=49,long=3)
    print('sunrise at ',s.sunrise(when=datetime.datetime.now())
    """

    def __init__(self, lat=50.24, long=18.83):  # default Amsterdam
        self.lat = lat
        self.long = long

    def sunrise(self, when=None):
        """
        return the time of sunrise as a datetime.time object
        when is a datetime.datetime object. If none is given
        a local time zone is assumed (including daylight saving
        if present)
        """
        if when is None: when = datetime.now()
        self.__preptime(when)
        self.__calc()
        return sun.__timefromdecimalday(self.sunrise_t)

    def sunset(self, when=None):
        if when is None: when = datetime.now()
        self.__preptime(when)
        self.__calc()
        return sun.__timefromdecimalday(self.sunset_t)

    def solarnoon(self, when=None):
        if when is None: when = datetime.now()
        self.__preptime(when)
        self.__calc()
        return sun.__timefromdecimalday(self.solarnoon_t)

    @staticmethod
    def __timefromdecimalday(day):
        """
        returns a datetime.time object.

        day is a decimal day between 0.0 and 1.0, e.g. noon = 0.5
        """
        hours = 24.0 * day
        h = int(hours)
        minutes = (hours - h) * 60
        m = int(minutes)
        seconds = (minutes - m) * 60
        s = int(seconds)
        return time(hour=h, minute=m, second=s)

    def __preptime(self, when):
        """
        Extract information in a suitable format from when,
        a datetime.datetime object.
        """
        # datetime days are numbered in the Gregorian calendar
        # while the calculations from NOAA are distibuted as
        # OpenOffice spreadsheets with days numbered from
        # 1/1/1900. The difference are those numbers taken for
        # 18/12/2010
        self.day = when.toordinal() - (734124 - 40529)
        t = when.time()
        self.time = (t.hour + t.minute / 60.0 + t.second / 3600.0) / 24.0

        self.timezone = 1
        offset = when.utcoffset()
        if not offset is None:
            self.timezone = offset.seconds / 3600.0

    def __calc(self):
        """
        Perform the actual calculations for sunrise, sunset and
        a number of related quantities.

        The results are stored in the instance variables
        sunrise_t, sunset_t and solarnoon_t
        """
        timezone = self.timezone  # in hours, east is positive
        longitude = self.long  # in decimal degrees, east is positive
        latitude = self.lat  # in decimal degrees, north is positive

        time = self.time  # percentage past midnight, i.e. noon  is 0.5
        day = self.day  # daynumber 1=1/1/1900

        Jday = day + 2415018.5 + time - timezone / 24  # Julian day
        Jcent = (Jday - 2451545) / 36525  # Julian century

        Manom = 357.52911 + Jcent * (35999.05029 - 0.0001537 * Jcent)
        Mlong = 280.46646 + Jcent * (36000.76983 + Jcent * 0.0003032) % 360
        Eccent = 0.016708634 - Jcent * (0.000042037 + 0.0001537 * Jcent)
        Mobliq = 23 + (26 + ((21.448 - Jcent * (46.815 + Jcent * (0.00059 - Jcent * 0.001813)))) / 60) / 60
        obliq = Mobliq + 0.00256 * cos(rad(125.04 - 1934.136 * Jcent))
        vary = tan(rad(obliq / 2)) * tan(rad(obliq / 2))
        Seqcent = sin(rad(Manom)) * (1.914602 - Jcent * (0.004817 + 0.000014 * Jcent)) + sin(rad(2 * Manom)) * (
                    0.019993 - 0.000101 * Jcent) + sin(rad(3 * Manom)) * 0.000289
        Struelong = Mlong + Seqcent
        Sapplong = Struelong - 0.00569 - 0.00478 * sin(rad(125.04 - 1934.136 * Jcent))
        declination = deg(asin(sin(rad(obliq)) * sin(rad(Sapplong))))

        eqtime = 4 * deg(
            vary * sin(2 * rad(Mlong)) - 2 * Eccent * sin(rad(Manom)) + 4 * Eccent * vary * sin(rad(Manom)) * cos(
                2 * rad(Mlong)) - 0.5 * vary * vary * sin(4 * rad(Mlong)) - 1.25 * Eccent * Eccent * sin(
                2 * rad(Manom)))

        hourangle = deg(acos(cos(rad(90.833)) / (cos(rad(latitude)) * cos(rad(declination))) - tan(rad(latitude)) * tan(
            rad(declination))))

        self.solarnoon_t = (720 - 4 * longitude - eqtime + timezone * 60) / 1440
        self.sunrise_t = self.solarnoon_t - hourangle * 4 / 1440
        self.sunset_t = self.solarnoon_t + hourangle * 4 / 1440


if __name__ == "__main__":
    czas1 = po_zach(50.25, 18.83)
    czas2 = po_wsch(50.25, 18.83)
    print(czas1,czas2)