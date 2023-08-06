# -*- coding: utf-8 -*-
import calendar
import re

from _strptime import (_calc_julian_from_U_or_W, _calc_julian_from_V, _cache_lock, _getlang, datetime_date, _CACHE_MAX_SIZE,
                       _regex_cache, _strptime_datetime, LocaleTime, re_escape, IGNORECASE, re_compile)
import time

import datetime

from warnings import warn
from bisect import bisect_right

from kanjize import kanji2int, int2kanji

class TimeRE(dict):
    """Handle conversion from format directives to regexes."""

    def __init__(self, locale_time=None):
        """Create keys/values.

        Order of execution is important for dependency reasons.

        """
        if locale_time:
            self.locale_time = locale_time
        else:
            self.locale_time = LocaleTime()
        base = super()
        base.__init__({
            # The " [1-9]" part of the regex is to make %c from ANSI C work
            'd': r"(?P<d>3[0-1]|[1-2]\d|0[1-9]|[1-9]| [1-9])",
            'f': r"(?P<f>[0-9]{1,6})",
            'H': r"(?P<H>2[0-3]|[0-1]\d|\d)",
            'I': r"(?P<I>1[0-2]|0[1-9]|[1-9])",
            'G': r"(?P<G>\d\d\d\d)",
            'j': r"(?P<j>36[0-6]|3[0-5]\d|[1-2]\d\d|0[1-9]\d|00[1-9]|[1-9]\d|0[1-9]|[1-9])",
            'm': r"(?P<m>1[0-2]|0[1-9]|[1-9])",
            'M': r"(?P<M>[0-5]\d|\d)",
            'S': r"(?P<S>6[0-1]|[0-5]\d|\d)",
            'U': r"(?P<U>5[0-3]|[0-4]\d|\d)",
            'w': r"(?P<w>[0-6])",
            'u': r"(?P<u>[1-7])",
            'V': r"(?P<V>5[0-3]|0[1-9]|[1-4]\d|\d)",
            # W is set below by using 'U'
            'y': r"(?P<y>\d\d|\d)",
            #XXX: Does 'Y' need to worry about having less or more than
            #     4 digits?
            'Y': r"(?P<Y>\d\d\d\d)",
            'z': r"(?P<z>[+-]\d\d:?[0-5]\d(:?[0-5]\d(\.\d{1,6})?)?|Z)",
            'A': self.__seqToRE(self.locale_time.f_weekday, 'A'),
            'a': self.__seqToRE(self.locale_time.a_weekday, 'a'),
            'B': self.__seqToRE(self.locale_time.f_month[1:], 'B'),
            'b': self.__seqToRE(self.locale_time.a_month[1:], 'b'),
            'p': self.__seqToRE(self.locale_time.am_pm, 'p'),
            'Z': self.__seqToRE((tz for tz_names in self.locale_time.timezone
                                        for tz in tz_names),
                                'Z'),
            '%': '%'})
        base.__setitem__('W', base.__getitem__('U').replace('U', 'W'))
        base.__setitem__('c', self.pattern(self.locale_time.LC_date_time))
        base.__setitem__('x', self.pattern(self.locale_time.LC_date))
        base.__setitem__('X', self.pattern(self.locale_time.LC_time))

    def __seqToRE(self, to_convert, directive):
        """Convert a list to a regex string for matching a directive.

        Want possible matching values to be from longest to shortest.  This
        prevents the possibility of a match occurring for a value that also
        a substring of a larger value that should have matched (e.g., 'abc'
        matching when 'abcdef' should have been the match).

        """
        to_convert = sorted(to_convert, key=len, reverse=True)
        for value in to_convert:
            if value != '':
                break
        else:
            return ''
        regex = '|'.join(re_escape(stuff) for stuff in to_convert)
        regex = '(?P<%s>%s' % (directive, regex)
        return '%s)' % regex

    def pattern(self, format):
        """Return regex pattern for the format string.

        Need to make sure that any characters that might be interpreted as
        regex syntax are escaped.

        """
        processed_format = ''
        # The sub() call escapes all characters that might be misconstrued
        # as regex syntax.  Cannot use re.escape since we have to deal with
        # format directives (%m, etc.).
        regex_chars = re_compile(r"([\\.^$*+?\(\){}\[\]|])")
        format = regex_chars.sub(r"\\\1", format)
        whitespace_replacement = re_compile(r'\s+')
        format = whitespace_replacement.sub(r'\\s+', format)
        while '%' in format:
            directive_index = format.index('%')+1
            processed_format = "%s%s%s" % (processed_format,
                                           format[:directive_index-1],
                                           self[format[directive_index]])
            format = format[directive_index+1:]
        return "%s%s" % (processed_format, format)

    def compile(self, format):
        """Return a compiled re object for the format string."""
        return re_compile(self.pattern(format), IGNORECASE)

_TimeRE_cache = TimeRE()


def _strptime(data_string, format="%a %b %d %H:%M:%S %Y"):
    """Return a 2-tuple consisting of a time struct and an int containing
    the number of microseconds based on the input string and the
    format string."""

    for index, arg in enumerate([data_string, format]):
        if not isinstance(arg, str):
            msg = "strptime() argument {} must be str, not {}"
            raise TypeError(msg.format(index, type(arg)))

    global _TimeRE_cache, _regex_cache
    with _cache_lock:
        locale_time = _TimeRE_cache.locale_time
        if (_getlang() != locale_time.lang or
                time.tzname != locale_time.tzname or
                time.daylight != locale_time.daylight):
            _TimeRE_cache = TimeRE()
            _regex_cache.clear()
            locale_time = _TimeRE_cache.locale_time
        if len(_regex_cache) > _CACHE_MAX_SIZE:
            _regex_cache.clear()
        format_regex = _regex_cache.get(format)
        if not format_regex:
            try:
                format_regex = _TimeRE_cache.compile(format)
            # KeyError raised when a bad format is found; can be specified as
            # \\, in which case it was a stray % but with a space after it
            except KeyError as err:
                bad_directive = err.args[0]
                if bad_directive == "\\":
                    bad_directive = "%"
                del err
                raise ValueError("'%s' is a bad directive in format '%s'" %
                                 (bad_directive, format)) from None
            # IndexError only occurs when the format string is "%"
            except IndexError:
                raise ValueError("stray %% in format '%s'" % format) from None
            _regex_cache[format] = format_regex
    found = format_regex.match(data_string)
    if not found:
        raise ValueError("time data %r does not match format %r" %
                         (data_string, format))
    if len(data_string) != found.end():
        raise ValueError("unconverted data remains: %s" %
                         data_string[found.end():])

    iso_year = year = None
    month = day = 1
    hour = minute = second = fraction = 0
    tz = -1
    gmtoff = None
    gmtoff_fraction = 0
    # Default to -1 to signify that values not known; not critical to have,
    # though
    iso_week = week_of_year = None
    week_of_year_start = None
    # weekday and julian defaulted to None so as to signal need to calculate
    # values
    weekday = julian = None
    found_dict = found.groupdict()
    for group_key in found_dict.keys():
        # Directives not explicitly handled below:
        #   c, x, X
        #      handled by making out of other directives
        #   U, W
        #      worthless without day of the week
        if group_key == 'y':
            year = int(found_dict['y'])
            # Open Group specification for strptime() states that a %y
            # value in the range of [00, 68] is in the century 2000, while
            # [69,99] is in the century 1900
            if year <= 68:
                year += 2000
            else:
                year += 1900
        elif group_key == 'Y':
            year = int(found_dict['Y'])
        elif group_key == 'G':
            iso_year = int(found_dict['G'])
        elif group_key == 'm':
            month = int(found_dict['m'])
        elif group_key == 'B':
            month = locale_time.f_month.index(found_dict['B'].lower())
        elif group_key == 'b':
            month = locale_time.a_month.index(found_dict['b'].lower())
        elif group_key == 'd':
            day = int(found_dict['d'])
        elif group_key == 'H':
            hour = int(found_dict['H'])
        elif group_key == 'I':
            hour = int(found_dict['I'])
            ampm = found_dict.get('p', '').lower()
            # If there was no AM/PM indicator, we'll treat this like AM
            if ampm in ('', locale_time.am_pm[0]):
                # We're in AM so the hour is correct unless we're
                # looking at 12 midnight.
                # 12 midnight == 12 AM == hour 0
                if hour == 12:
                    hour = 0
            elif ampm == locale_time.am_pm[1]:
                # We're in PM so we need to add 12 to the hour unless
                # we're looking at 12 noon.
                # 12 noon == 12 PM == hour 12
                if hour != 12:
                    hour += 12
        elif group_key == 'M':
            minute = int(found_dict['M'])
        elif group_key == 'S':
            second = int(found_dict['S'])
        elif group_key == 'f':
            s = found_dict['f']
            # Pad to always return microseconds.
            s += "0" * (6 - len(s))
            fraction = int(s)
        elif group_key == 'A':
            weekday = locale_time.f_weekday.index(found_dict['A'].lower())
        elif group_key == 'a':
            weekday = locale_time.a_weekday.index(found_dict['a'].lower())
        elif group_key == 'w':
            weekday = int(found_dict['w'])
            if weekday == 0:
                weekday = 6
            else:
                weekday -= 1
        elif group_key == 'u':
            weekday = int(found_dict['u'])
            weekday -= 1
        elif group_key == 'j':
            julian = int(found_dict['j'])
        elif group_key in ('U', 'W'):
            week_of_year = int(found_dict[group_key])
            if group_key == 'U':
                # U starts week on Sunday.
                week_of_year_start = 6
            else:
                # W starts week on Monday.
                week_of_year_start = 0
        elif group_key == 'V':
            iso_week = int(found_dict['V'])
        elif group_key == 'z':
            z = found_dict['z']
            if z == 'Z':
                gmtoff = 0
            else:
                if z[3] == ':':
                    z = z[:3] + z[4:]
                    if len(z) > 5:
                        if z[5] != ':':
                            msg = f"Inconsistent use of : in {found_dict['z']}"
                            raise ValueError(msg)
                        z = z[:5] + z[6:]
                hours = int(z[1:3])
                minutes = int(z[3:5])
                seconds = int(z[5:7] or 0)
                gmtoff = (hours * 60 * 60) + (minutes * 60) + seconds
                gmtoff_remainder = z[8:]
                # Pad to always return microseconds.
                gmtoff_remainder_padding = "0" * (6 - len(gmtoff_remainder))
                gmtoff_fraction = int(gmtoff_remainder + gmtoff_remainder_padding)
                if z.startswith("-"):
                    gmtoff = -gmtoff
                    gmtoff_fraction = -gmtoff_fraction
        elif group_key == 'Z':
            # Since -1 is default value only need to worry about setting tz if
            # it can be something other than -1.
            found_zone = found_dict['Z'].lower()
            for value, tz_values in enumerate(locale_time.timezone):
                if found_zone in tz_values:
                    # Deal with bad locale setup where timezone names are the
                    # same and yet time.daylight is true; too ambiguous to
                    # be able to tell what timezone has daylight savings
                    if (time.tzname[0] == time.tzname[1] and
                            time.daylight and found_zone not in ("utc", "gmt")):
                        break
                    else:
                        tz = value
                        break
    # Deal with the cases where ambiguities arize
    # don't assume default values for ISO week/year
    if year is None and iso_year is not None:
        if iso_week is None or weekday is None:
            raise ValueError("ISO year directive '%G' must be used with "
                             "the ISO week directive '%V' and a weekday "
                             "directive ('%A', '%a', '%w', or '%u').")
        if julian is not None:
            raise ValueError("Day of the year directive '%j' is not "
                             "compatible with ISO year directive '%G'. "
                             "Use '%Y' instead.")
    elif week_of_year is None and iso_week is not None:
        if weekday is None:
            raise ValueError("ISO week directive '%V' must be used with "
                             "the ISO year directive '%G' and a weekday "
                             "directive ('%A', '%a', '%w', or '%u').")
        else:
            raise ValueError("ISO week directive '%V' is incompatible with "
                             "the year directive '%Y'. Use the ISO year '%G' "
                             "instead.")

    leap_year_fix = False
    if year is None and month == 2 and day == 29:
        year = 1904  # 1904 is first leap year of 20th century
        leap_year_fix = True
    elif year is None:
        year = 1900

    # If we know the week of the year and what day of that week, we can figure
    # out the Julian day of the year.
    if julian is None and weekday is not None:
        if week_of_year is not None:
            week_starts_Mon = True if week_of_year_start == 0 else False
            julian = _calc_julian_from_U_or_W(year, week_of_year, weekday,
                                              week_starts_Mon)
        elif iso_year is not None and iso_week is not None:
            year, julian = _calc_julian_from_V(iso_year, iso_week, weekday + 1)
        if julian is not None and julian <= 0:
            year -= 1
            yday = 366 if calendar.isleap(year) else 365
            julian += yday
    return (year, month, day,
            hour, minute, second,
            weekday, julian, tz, gmtoff), fraction, gmtoff_fraction


class EraDate(datetime.date):
    def __new__(cls, year, month=None, day=None, era=None, use_chris=True):
        self = super().__new__(cls, year, month, day)
        if not era:
            self.era = Japanera().era(self, use_chris)
        else:
            self.era = era
        if self.era.is_after(self):
            warn("Given era is not seems match for this date")
        return self

    def strftime(self, fmt, allow_before=False):
        """
        %-E: Kanji era name
        %-e: Alphabet era name vowel shortened
        %-A: Alphabet era name
        %-a: First letter of alphabet era name
        %-o: Two digit year of corresponding era
        %-O: Two digit year of corresponding era. But return "元" for the first year
        %-ko: Two digit year of corresponding era in Kanji
        %-kO: Two digit year of corresponding era in Kanji. But return "元" for the first year
        %-km: Month of date in Kanji
        %-kd: Day of date in Kanji
        + datetime.strftime's format

        allow_before: object can be converted to bool. If it's True and the given dt if before than self,start,
                     %-o and %-O will be "Unknown". If False, raise an ValueError. Default: False
        """
        try:
            year = self.year - self.era.start.year + 1
            rep = {"%-E": self.era.kanji, "%-e": self.era.english_shorten_vowel, "%-A": self.era.english,
                   "%-a": self.era.english[0], "%-o": str(year % 100).zfill(2),
                   "%-O": "元" if year == 1 else str(year % 100).zfill(2), "%-ko": int2kanji(year % 100),
                   "%-kO": "元" if year == 1 else int2kanji(year % 100), "%-km": int2kanji(self.month),
                   "%-kd": int2kanji(self.day)}
        except (AttributeError, TypeError):
            try:
                rep = {"%-E": "不明", "%-e": "Unknown", "%-A": "Unknown", "%-a": "U", "%-o": str(year % 100).zfill(2),
                       "%-O": "元" if year == 1 else str(year % 100).zfill(2), "%-ko": int2kanji(year % 100),
                       "%-kO": "元" if year == 1 else int2kanji(year % 100), "%-km": int2kanji(self.month),
                       "%-kd": int2kanji(self.day)}
            except (AttributeError, UnboundLocalError):
                if not allow_before:
                    raise ValueError("Given date is too early to format")
                rep = {"%-E": "不明", "%-e": "Unknown", "%-A": "Unknown", "%-a": "U", "%-o": "Unknown",
                       "%-O": "Unknown", "%-ko": "不明",
                       "%-kO": "不明", "%-km": "不明",
                       "%-kd": "不明"}

        rep = dict((re.escape(k), str(v)) for k, v in rep.items())
        pattern = re.compile("|".join(rep.keys()))
        return datetime.datetime.strftime(self, pattern.sub(lambda m: rep[re.escape(m.group(0))], fmt))

    @classmethod
    def fromdate(cls, dt, era=None, use_chris=True):
        if not era:
            era = Japanera().era(dt)
        return cls(year=dt.year, month=dt.month, day=dt.day, era=era, use_chris=use_chris)

    def todate(self):
        return datetime.date(year=self.year, month=self.month, day=self.day)

    def __repr__(self):
        return "Era.eradate({}, {}, {}, {})".format(self.era, self.year, self.month, self.day)

    def __str__(self):
        return self.strftime("%-E-%Y-%m-%d")


class EraDateTime(datetime.datetime):
    def __new__(cls, year, month=None, day=None, hour=0, minute=0, second=0,
                microsecond=0, tzinfo=None, *, fold=0, era=None, use_chris=True):
        self = super().__new__(cls, year=year, month=month, day=day, hour=hour, minute=minute, second=second,
                               microsecond=microsecond, tzinfo=tzinfo, fold=fold)
        if not era:
            self.era = Japanera().era(self, use_chris)
        else:
            self.era = era
        if self.era.is_after(self):
            warn("Given era is not seems match for this date")
        return self

    def strftime(self, fmt, allow_before=False):
        """
        %-E: Kanji era name
        %-e: Alphabet era name vowel shortened
        %-A: Alphabet era name
        %-a: First letter of alphabet era name
        %-o: Two digit year of corresponding era
        %-O: Two digit year of corresponding era. But return "元" for the first year
        %-ko: Two digit year of corresponding era in Kanji
        %-kO: Two digit year of corresponding era in Kanji. But return "元" for the first year
        %-km: Month of date in Kanji
        %-kd: Day of date in Kanji
        + datetime.strftime's format

        allow_before: object can be converted to bool. If it's True and the given dt if before than self,start,
                     %-o and %-O will be "Unknown". If False, raise an ValueError. Default: False
        """
        try:
            year = self.year - self.era.start.year + 1
            rep = {"%-E": self.era.kanji, "%-e": self.era.english_shorten_vowel, "%-A": self.era.english,
                   "%-a": self.era.english[0], "%-o": str(year % 100).zfill(2),
                   "%-O": "元" if year == 1 else str(year % 100).zfill(2), "%-ko": int2kanji(year % 100),
                   "%-kO": "元" if year == 1 else int2kanji(year % 100), "%-km": int2kanji(self.month),
                   "%-kd": int2kanji(self.day)}
        except (AttributeError, TypeError):
            try:
                rep = {"%-E": "不明", "%-e": "Unknown", "%-A": "Unknown", "%-a": "U", "%-o": str(year % 100).zfill(2),
                       "%-O": "元" if year == 1 else str(year % 100).zfill(2), "%-ko": int2kanji(year % 100),
                       "%-kO": "元" if year == 1 else int2kanji(year % 100), "%-km": int2kanji(self.month),
                       "%-kd": int2kanji(self.day)}
            except (AttributeError, UnboundLocalError):
                if not allow_before:
                    raise ValueError("Given date is too early to format")
                rep = {"%-E": "不明", "%-e": "Unknown", "%-A": "Unknown", "%-a": "U", "%-o": "Unknown",
                       "%-O": "Unknown", "%-ko": "不明",
                       "%-kO": "不明", "%-km": "不明",
                       "%-kd": "不明"}

        rep = dict((re.escape(k), str(v)) for k, v in rep.items())
        pattern = re.compile("|".join(rep.keys()))
        return datetime.datetime.strftime(self, pattern.sub(lambda m: rep[re.escape(m.group(0))], fmt))

    @classmethod
    def fromdatetime(cls, dtt, era=None, use_chris=True):
        if not era:
            era = Japanera().era(dtt)
        return cls(year=dtt.year, month=dtt.month, day=dtt.day, hour=dtt.hour, minute=dtt.minute, second=dtt.second,
                   microsecond=dtt.microsecond, tzinfo=dtt.tzinfo, fold=dtt.fold, era=era, use_chris=use_chris)

    def todatetime(self):
        return datetime.datetime(year=self.year, month=self.month, day=self.day, hour=self.hour, minute=self.minute,
                                 second=self.second, microsecond=self.microsecond, tzinfo=self.tzinfo, fold=self.fold)

    def __repr__(self):
        return "Era.eradate({}, {}, {}, {}, {}, {}, {}, {})".format(self.era, self.year, self.month, self.day,
                                                                    self.hour, self.minute, self.second,
                                                                    self.microsecond)

    def __str__(self):
        return self.strftime("%-E-%Y-%m-%d %H:%M:%S")


class Era:
    def __init__(self, kanji, english, start, end, _type):
        """

        :param kanji - str: kanji letter of era. exp. "大正"
        :param english - str: english letter of pronunciation of era. exp. "Taishou"
        :param start - datetime.date: start of the era. This day is included to this era.
        :param end - datetime.date: end of the era. This day is excluded to this era.
        :param _type - str: Type of This Era. "common", "daikakuji", "jimyouin"  or "christian"
        """
        self.kanji = kanji
        self.english = english
        self.start = start
        self.end = end
        self.type = _type

    @property
    def english_shorten_vowel(self):
        """
        Return self.english vowel shortened. exp. "Taishou" -> "Taisho"
        :return: str

        Didn't use str.replace for scalability
        """
        try:
            english = self.english.lower()
        except AttributeError:
            return None

        table = {"ou": "o", "uu": "u"}

        pattern = re.compile("|".join(table.keys()))
        return pattern.sub(lambda m: table[re.escape(m.group(0))], english).title()

    @property
    def english_head(self):
        """
        Return the first letter of self.english
        :return:
        """
        return self.english[0]

    def _in(self, dt):
        """
        Return if given date is in between self.start and self.end
        :param dt: datetime.date or datetime.datetime
        :return: bool
        """
        if isinstance(dt, datetime.datetime):
            dt = dt.date()
        if self.start and self.end:
            return self.start <= dt < self.end
        elif self.start:
            return self.start <= dt
        elif self.end:
            return dt < self.end
        return False

    def is_after(self, other):
        """
        Return if given object (datetime.date or japanera.Era) is placed after this era.
        :param other - datetime.date or japanera.Era:
        :return: bool
        """
        return other < self

    def is_before(self, other):
        """
        Return if given object (datetime.date or japanera.Era) is placed before this era.
        :param other - datetime.date or japanera.Era:
        :return: bool
        """
        return self < other

    def strftime(self, dt, fmt, allow_before=False):
        """
        %-E: Kanji era name
        %-e: Alphabet era name vowel shortened
        %-A: Alphabet era name
        %-a: First letter of alphabet era name
        %-o: Two digit year of corresponding era
        %-O: Two digit year of corresponding era. But return "元" for the first year
        %-ko: Two digit year of corresponding era in Kanji
        %-kO: Two digit year of corresponding era in Kanji. But return "元" for the first year
        %-km: Month of date in Kanji
        %-kd: Day of date in Kanji
        + datetime.strftime's format

        allow_before: object can be converted to bool. If it's True and the given dt if before than self,start,
                     %-o and %-O will be "Unknown". If False, raise an ValueError. Default: False
        """
        if isinstance(dt, datetime.datetime):
            return EraDateTime.fromdatetime(dt, self).strftime(fmt, allow_before)
        return EraDate.fromdate(dt, self).strftime(fmt, allow_before)

    def strptime(self, _str, fmt):
        """
        %-E: Kanji era name
        %-e: Alphabet era name vowel shortened
        %-A: Alphabet era name
        %-a: First letter of alphabet era name
        %-o: Two digit year of corresponding era
        %-O: Two digit year of corresponding era. But return "元" for the first year
        %-ko: Two digit year of corresponding era in Kanji
        %-kO: Two digit year of corresponding era in Kanji. But return "元" for the first year
        %-km: Month of date in Kanji
        %-kd: Day of date in Kanji
        + datetime.strftime's format
        """
        try:
            rep = {"%-E": self.kanji, "%-A": self.english, "%-a": self.english[0], "%-s": self.english_shorten_vowel,
                   "%-o": "%y", "%-O": "%y", "%-ko": "%y", "%-kO": "%y", "%-km": "%m", "%-kd": "%d"}
        except TypeError:
            rep = {"%-E": "不明", "%-A": "Unknown", "%-a": "U", "%-s": "Unknown", "%-o": "%y", "%-O": "%y",
                   "%-ko": "%y", "%-kO": "%y", "%-km": "%m", "%-kd": "%d"}

        if "%-O" in fmt or "%-kO" in fmt:
            fmt = fmt.replace("元", "01")
            _str = _str.replace("元", "01")

        kanjis = re.compile("[一二三四五六七八九十百千万億兆京垓𥝱]+").findall(_str)
        int_from_kanji = [*map(lambda x: str(kanji2int(x)).zfill(2), kanjis)]
        for k, i in zip(kanjis, int_from_kanji):
            _str = _str.replace(k, str(i))
            fmt = fmt.replace(k, str(i))

        rep = dict((re.escape(k), str(v)) for k, v in rep.items())
        pattern = re.compile("|".join(rep.keys()))
        fmt = pattern.sub(lambda m: rep[re.escape(m.group(0))], fmt)

        dt = datetime.datetime.strptime(_str, fmt)
        if "%y" in fmt:
            dt = dt.replace(year=(dt.year % 100) + self.start.year - 1)
        return dt

    def __gt__(self, other):
        if isinstance(other, Era):
            return other.end < self.start
        elif isinstance(other, datetime.datetime):
            return other.date() < self.start
        elif isinstance(other, datetime.date):
            return other < self.start

    def __lt__(self, other):
        if not self.end:
            return False
        if isinstance(other, Era):
            return self.end < other.start
        elif isinstance(other, datetime.datetime):
            return self.end < other.date()
        elif isinstance(other, datetime.date):
            return self.end < other

    def __eq__(self, other):
        try:
            for key in ("kanji", "english", "start", "end", "type"):
                if getattr(self, key) != getattr(other, key):
                    return False
            return True
        except AttributeError:
            return False

    def __repr__(self):
        start_time = self.start.strftime("%d/%m/%Y") if self.start else "None"
        end_time = self.end.strftime("%d/%m/%Y") if self.end else "None"
        return "<Era {}:{} {} - {}>".format(self.kanji, self.english, start_time, end_time)

    def __str__(self):
        return "{}: {}".format(self.kanji, self.english)


class Japanera:
    era_common = [Era("大化", "Taika", datetime.date(645, 7, 20), datetime.date(650, 3, 25), "common"),
                  Era("白雉", "Hakuchi", datetime.date(650, 3, 25), datetime.date(654, 11, 27), "common"),
                  Era(None, None, datetime.date(654, 11, 27), datetime.date(686, 8, 17), "common"),
                  Era("朱鳥", "Shuchou", datetime.date(686, 8, 17), datetime.date(686, 10, 4), "common"),
                  Era(None, None, datetime.date(686, 10, 4), datetime.date(701, 5, 7), "common"),
                  Era("大宝", "Taihou", datetime.date(701, 5, 7), datetime.date(704, 6, 20), "common"),
                  Era("慶雲", "Keiun", datetime.date(704, 6, 20), datetime.date(708, 2, 11), "common"),
                  Era("和銅", "Wadou", datetime.date(708, 2, 11), datetime.date(715, 10, 7), "common"),
                  Era("霊亀", "Reiki", datetime.date(715, 10, 7), datetime.date(717, 12, 28), "common"),
                  Era("養老", "Yourou", datetime.date(717, 12, 28), datetime.date(724, 3, 7), "common"),
                  Era("神亀", "Jinki", datetime.date(724, 3, 7), datetime.date(729, 9, 6), "common"),
                  Era("天平", "Tempyou", datetime.date(729, 9, 6), datetime.date(749, 5, 8), "common"),
                  Era("天平感宝", "TempyouKampou", datetime.date(749, 5, 8), datetime.date(749, 8, 23), "common"),
                  Era("天平勝宝", "TempyouSyouhou", datetime.date(749, 8, 23), datetime.date(757, 9, 10), "common"),
                  Era("天平宝字", "TempyouHouji", datetime.date(757, 9, 10), datetime.date(765, 2, 5), "common"),
                  Era("天平神護", "TempyouJingo", datetime.date(765, 2, 5), datetime.date(767, 9, 17), "common"),
                  Era("神護景雲", "JingoKeiun", datetime.date(767, 9, 17), datetime.date(770, 10, 27), "common"),
                  Era("宝亀", "Houki", datetime.date(770, 10, 27), datetime.date(781, 2, 3), "common"),
                  Era("天応", "Tennou", datetime.date(781, 2, 3), datetime.date(782, 10, 4), "common"),
                  Era("延暦", "Enryaku", datetime.date(782, 10, 4), datetime.date(806, 6, 12), "common"),
                  Era("大同", "Daidou", datetime.date(806, 6, 12), datetime.date(810, 10, 24), "common"),
                  Era("弘仁", "Kounin", datetime.date(810, 10, 24), datetime.date(824, 2, 12), "common"),
                  Era("天長", "Tenchou", datetime.date(824, 2, 12), datetime.date(834, 2, 18), "common"),
                  Era("承和", "Jouwa", datetime.date(834, 2, 18), datetime.date(848, 7, 20), "common"),
                  Era("嘉祥", "Kashou", datetime.date(848, 7, 20), datetime.date(851, 6, 5), "common"),
                  Era("仁寿", "Ninju", datetime.date(851, 6, 5), datetime.date(854, 12, 27), "common"),
                  Era("斉衡", "Saikou", datetime.date(854, 12, 27), datetime.date(857, 3, 24), "common"),
                  Era("天安", "Tennan", datetime.date(857, 3, 24), datetime.date(859, 5, 24), "common"),
                  Era("貞観", "Jougan", datetime.date(859, 5, 24), datetime.date(877, 6, 5), "common"),
                  Era("元慶", "Gangyou", datetime.date(877, 6, 5), datetime.date(885, 3, 15), "common"),
                  Era("仁和", "Ninna", datetime.date(885, 3, 15), datetime.date(889, 6, 3), "common"),
                  Era("寛平", "Kampyou", datetime.date(889, 6, 3), datetime.date(898, 5, 24), "common"),
                  Era("昌泰", "Syoutai", datetime.date(898, 5, 24), datetime.date(901, 9, 5), "common"),
                  Era("延喜", "Engi", datetime.date(901, 9, 5), datetime.date(923, 6, 3), "common"),
                  Era("延長", "Enchou", datetime.date(923, 6, 3), datetime.date(931, 5, 21), "common"),
                  Era("承平", "Jouhei", datetime.date(931, 5, 21), datetime.date(938, 6, 27), "common"),
                  Era("天慶", "Tengyou", datetime.date(938, 6, 27), datetime.date(947, 5, 20), "common"),
                  Era("天暦", "Tenryaku", datetime.date(947, 5, 20), datetime.date(957, 11, 26), "common"),
                  Era("天徳", "Tentoku", datetime.date(957, 11, 26), datetime.date(961, 3, 10), "common"),
                  Era("応和", "Ouwa", datetime.date(961, 3, 10), datetime.date(964, 8, 24), "common"),
                  Era("康保", "Kouhou", datetime.date(964, 8, 24), datetime.date(968, 9, 13), "common"),
                  Era("安和", "Anna", datetime.date(968, 9, 13), datetime.date(970, 5, 8), "common"),
                  Era("天禄", "Tenroku", datetime.date(970, 5, 8), datetime.date(974, 1, 21), "common"),
                  Era("天延", "Tenen", datetime.date(974, 1, 21), datetime.date(976, 8, 16), "common"),
                  Era("貞元", "Jougen", datetime.date(976, 8, 16), datetime.date(979, 1, 5), "common"),
                  Era("天元", "Tengen", datetime.date(979, 1, 5), datetime.date(983, 6, 3), "common"),
                  Era("永観", "Eikan", datetime.date(983, 6, 3), datetime.date(985, 5, 24), "common"),
                  Era("寛和", "Kanna", datetime.date(985, 5, 24), datetime.date(987, 5, 10), "common"),
                  Era("永延", "Eien", datetime.date(987, 5, 10), datetime.date(989, 9, 15), "common"),
                  Era("永祚", "Eiso", datetime.date(989, 9, 15), datetime.date(990, 12, 1), "common"),
                  Era("正暦", "Syouryaku", datetime.date(990, 12, 1), datetime.date(995, 3, 30), "common"),
                  Era("長徳", "Choutoku", datetime.date(995, 3, 30), datetime.date(999, 2, 6), "common"),
                  Era("長保", "Chouhou", datetime.date(999, 2, 6), datetime.date(1004, 8, 14), "common"),
                  Era("寛弘", "Kankou", datetime.date(1004, 8, 14), datetime.date(1013, 2, 14), "common"),
                  Era("長和", "Chouwa", datetime.date(1013, 2, 14), datetime.date(1017, 5, 27), "common"),
                  Era("寛仁", "Kannin", datetime.date(1017, 5, 27), datetime.date(1021, 3, 23), "common"),
                  Era("治安", "Jian", datetime.date(1021, 3, 23), datetime.date(1024, 8, 25), "common"),
                  Era("万寿", "Manju", datetime.date(1024, 8, 25), datetime.date(1028, 8, 24), "common"),
                  Era("長元", "Chougen", datetime.date(1028, 8, 24), datetime.date(1037, 5, 15), "common"),
                  Era("長暦", "Chouryaku", datetime.date(1037, 5, 15), datetime.date(1040, 12, 22), "common"),
                  Era("長久", "Choukyuu", datetime.date(1040, 12, 22), datetime.date(1044, 12, 22), "common"),
                  Era("寛徳", "Kantoku", datetime.date(1044, 12, 22), datetime.date(1046, 5, 28), "common"),
                  Era("永承", "Eishou", datetime.date(1046, 5, 28), datetime.date(1053, 2, 8), "common"),
                  Era("天喜", "Tenki", datetime.date(1053, 2, 8), datetime.date(1058, 9, 25), "common"),
                  Era("康平", "Kouhei", datetime.date(1058, 9, 25), datetime.date(1065, 9, 10), "common"),
                  Era("治暦", "Jiryaku", datetime.date(1065, 9, 10), datetime.date(1069, 5, 12), "common"),
                  Era("延久", "Enkyuu", datetime.date(1069, 5, 12), datetime.date(1074, 9, 22), "common"),
                  Era("承保", "Jouhou", datetime.date(1074, 9, 22), datetime.date(1077, 12, 11), "common"),
                  Era("承暦", "Jouryaku", datetime.date(1077, 12, 11), datetime.date(1081, 3, 28), "common"),
                  Era("永保", "Eihou", datetime.date(1081, 3, 28), datetime.date(1084, 3, 21), "common"),
                  Era("応徳", "Outoku", datetime.date(1084, 3, 21), datetime.date(1087, 5, 17), "common"),
                  Era("寛治", "Kanji", datetime.date(1087, 5, 17), datetime.date(1095, 1, 29), "common"),
                  Era("嘉保", "Kahou", datetime.date(1095, 1, 29), datetime.date(1097, 1, 9), "common"),
                  Era("永長", "Eichou", datetime.date(1097, 1, 9), datetime.date(1098, 1, 2), "common"),
                  Era("承徳", "Joutoku", datetime.date(1098, 1, 2), datetime.date(1099, 9, 21), "common"),
                  Era("康和", "Kouwa", datetime.date(1099, 9, 21), datetime.date(1104, 3, 15), "common"),
                  Era("長治", "Chouji", datetime.date(1104, 3, 15), datetime.date(1106, 5, 20), "common"),
                  Era("嘉承", "Kashou", datetime.date(1106, 5, 20), datetime.date(1108, 9, 16), "common"),
                  Era("天仁", "Tennin", datetime.date(1108, 9, 16), datetime.date(1110, 8, 7), "common"),
                  Era("天永", "Tennei", datetime.date(1110, 8, 7), datetime.date(1113, 9, 1), "common"),
                  Era("永久", "Eikyuu", datetime.date(1113, 9, 1), datetime.date(1118, 5, 2), "common"),
                  Era("元永", "Gennei", datetime.date(1118, 5, 2), datetime.date(1120, 5, 16), "common"),
                  Era("保安", "Houan", datetime.date(1120, 5, 16), datetime.date(1124, 5, 25), "common"),
                  Era("天治", "Tenji", datetime.date(1124, 5, 25), datetime.date(1126, 2, 22), "common"),
                  Era("大治", "Daiji", datetime.date(1126, 2, 22), datetime.date(1131, 3, 7), "common"),
                  Era("天承", "Tenshou", datetime.date(1131, 3, 7), datetime.date(1132, 9, 28), "common"),
                  Era("長承", "Choushou", datetime.date(1132, 9, 28), datetime.date(1135, 6, 17), "common"),
                  Era("保延", "Houen", datetime.date(1135, 6, 17), datetime.date(1141, 8, 20), "common"),
                  Era("永治", "Eiji", datetime.date(1141, 8, 20), datetime.date(1142, 6, 1), "common"),
                  Era("康治", "Kouji", datetime.date(1142, 6, 1), datetime.date(1144, 4, 4), "common"),
                  Era("天養", "Tennyou", datetime.date(1144, 4, 4), datetime.date(1145, 8, 19), "common"),
                  Era("久安", "Kyuuan", datetime.date(1145, 8, 19), datetime.date(1151, 2, 21), "common"),
                  Era("仁平", "Ninmpei", datetime.date(1151, 2, 21), datetime.date(1154, 12, 11), "common"),
                  Era("久寿", "Kyuuju", datetime.date(1154, 12, 11), datetime.date(1156, 5, 25), "common"),
                  Era("保元", "Hougen", datetime.date(1156, 5, 25), datetime.date(1159, 5, 16), "common"),
                  Era("平治", "Heiji", datetime.date(1159, 5, 16), datetime.date(1160, 2, 25), "common"),
                  Era("永暦", "Eiryaku", datetime.date(1160, 2, 25), datetime.date(1161, 10, 1), "common"),
                  Era("応保", "Ouhou", datetime.date(1161, 10, 1), datetime.date(1163, 5, 11), "common"),
                  Era("長寛", "Choukan", datetime.date(1163, 5, 11), datetime.date(1165, 7, 21), "common"),
                  Era("永万", "Eiman", datetime.date(1165, 7, 21), datetime.date(1166, 9, 30), "common"),
                  Era("仁安", "Ninnan", datetime.date(1166, 9, 30), datetime.date(1169, 5, 13), "common"),
                  Era("嘉応", "Kaou", datetime.date(1169, 5, 13), datetime.date(1171, 6, 3), "common"),
                  Era("承安", "Syouan", datetime.date(1171, 6, 3), datetime.date(1175, 8, 23), "common"),
                  Era("安元", "Angen", datetime.date(1175, 8, 23), datetime.date(1177, 9, 5), "common"),
                  Era("治承", "Jishou", datetime.date(1177, 9, 5), datetime.date(1181, 9, 1), "common"),
                  Era("養和", "Youwa", datetime.date(1181, 9, 1), datetime.date(1182, 7, 6), "common"),
                  Era("寿永", "Juei", datetime.date(1182, 7, 6), datetime.date(1184, 6, 3), "common"),
                  Era("元暦", "Genryaku", datetime.date(1184, 6, 3), datetime.date(1185, 9, 16), "common"),
                  Era("文治", "Bunji", datetime.date(1185, 9, 16), datetime.date(1190, 5, 23), "common"),
                  Era("建久", "Kenkyuu", datetime.date(1190, 5, 23), datetime.date(1199, 5, 30), "common"),
                  Era("正治", "Syouji", datetime.date(1199, 5, 30), datetime.date(1201, 3, 26), "common"),
                  Era("建仁", "Kennin", datetime.date(1201, 3, 26), datetime.date(1204, 3, 30), "common"),
                  Era("元久", "Genkyuu", datetime.date(1204, 3, 30), datetime.date(1206, 6, 12), "common"),
                  Era("建永", "Kennei", datetime.date(1206, 6, 12), datetime.date(1207, 11, 23), "common"),
                  Era("承元", "Jougen", datetime.date(1207, 11, 23), datetime.date(1211, 4, 30), "common"),
                  Era("建暦", "Kenryaku", datetime.date(1211, 4, 30), datetime.date(1214, 1, 25), "common"),
                  Era("建保", "Kempou", datetime.date(1214, 1, 25), datetime.date(1219, 6, 3), "common"),
                  Era("承久", "Joukyuu", datetime.date(1219, 6, 3), datetime.date(1222, 6, 1), "common"),
                  Era("貞応", "Jouou", datetime.date(1222, 6, 1), datetime.date(1225, 1, 7), "common"),
                  Era("元仁", "Gennin", datetime.date(1225, 1, 7), datetime.date(1225, 6, 4), "common"),
                  Era("嘉禄", "Karoku", datetime.date(1225, 6, 4), datetime.date(1228, 1, 25), "common"),
                  Era("安貞", "Antei", datetime.date(1228, 1, 25), datetime.date(1229, 4, 7), "common"),
                  Era("寛喜", "Kanki", datetime.date(1229, 4, 7), datetime.date(1232, 4, 30), "common"),
                  Era("貞永", "Jouei", datetime.date(1232, 4, 30), datetime.date(1233, 6, 1), "common"),
                  Era("天福", "Tempuku", datetime.date(1233, 6, 1), datetime.date(1234, 12, 4), "common"),
                  Era("文暦", "Bunryaku", datetime.date(1234, 12, 4), datetime.date(1235, 11, 8), "common"),
                  Era("嘉禎", "Katei", datetime.date(1235, 11, 8), datetime.date(1239, 1, 6), "common"),
                  Era("暦仁", "Ryakunin", datetime.date(1239, 1, 6), datetime.date(1239, 3, 20), "common"),
                  Era("延応", "Ennou", datetime.date(1239, 3, 20), datetime.date(1240, 8, 12), "common"),
                  Era("仁治", "Ninji", datetime.date(1240, 8, 12), datetime.date(1243, 3, 25), "common"),
                  Era("寛元", "Kangen", datetime.date(1243, 3, 25), datetime.date(1247, 4, 12), "common"),
                  Era("宝治", "Houji", datetime.date(1247, 4, 12), datetime.date(1249, 5, 9), "common"),
                  Era("建長", "Kenchou", datetime.date(1249, 5, 9), datetime.date(1256, 10, 31), "common"),
                  Era("康元", "Kougen", datetime.date(1256, 10, 31), datetime.date(1257, 4, 7), "common"),
                  Era("正嘉", "Syouka", datetime.date(1257, 4, 7), datetime.date(1259, 4, 27), "common"),
                  Era("正元", "Syougen", datetime.date(1259, 4, 27), datetime.date(1260, 5, 31), "common"),
                  Era("文応", "Bunnou", datetime.date(1260, 5, 31), datetime.date(1261, 3, 29), "common"),
                  Era("弘長", "Kouchou", datetime.date(1261, 3, 29), datetime.date(1264, 4, 3), "common"),
                  Era("文永", "Bunnei", datetime.date(1264, 4, 3), datetime.date(1275, 5, 29), "common"),
                  Era("建治", "Kenji", datetime.date(1275, 5, 29), datetime.date(1278, 3, 30), "common"),
                  Era("弘安", "Kouan", datetime.date(1278, 3, 30), datetime.date(1288, 6, 5), "common"),
                  Era("正応", "Syouou", datetime.date(1288, 6, 5), datetime.date(1293, 9, 13), "common"),
                  Era("永仁", "Einin", datetime.date(1293, 9, 13), datetime.date(1299, 6, 1), "common"),
                  Era("正安", "Syouan", datetime.date(1299, 6, 1), datetime.date(1302, 12, 18), "common"),
                  Era("乾元", "Kengen", datetime.date(1302, 12, 18), datetime.date(1303, 9, 24), "common"),
                  Era("嘉元", "Kagen", datetime.date(1303, 9, 24), datetime.date(1307, 1, 26), "common"),
                  Era("徳治", "Tokuji", datetime.date(1307, 1, 26), datetime.date(1308, 11, 30), "common"),
                  Era("延慶", "Enkyou", datetime.date(1308, 11, 30), datetime.date(1311, 5, 25), "common"),
                  Era("応長", "Ouchou", datetime.date(1311, 5, 25), datetime.date(1312, 5, 5), "common"),
                  Era("正和", "Syouwa", datetime.date(1312, 5, 5), datetime.date(1317, 3, 24), "common"),
                  Era("文保", "Bumpou", datetime.date(1317, 3, 24), datetime.date(1319, 5, 26), "common"),
                  Era("元応", "Gennou", datetime.date(1319, 5, 26), datetime.date(1321, 3, 30), "common"),
                  Era("元亨", "Gennkou", datetime.date(1321, 3, 30), datetime.date(1325, 1, 2), "common"),
                  Era("正中", "Syouchuu", datetime.date(1325, 1, 2), datetime.date(1326, 6, 5), "common"),
                  Era("嘉暦", "Karyaku", datetime.date(1326, 6, 5), datetime.date(1329, 9, 30), "common"),
                  Era("応永", "Ouei", datetime.date(1394, 8, 10), datetime.date(1428, 6, 19), "common"),
                  Era("正長", "Syouchou", datetime.date(1428, 6, 19), datetime.date(1429, 10, 12), "common"),
                  Era("永享", "Eikyou", datetime.date(1429, 10, 12), datetime.date(1441, 3, 19), "common"),
                  Era("嘉吉", "Kakitsu", datetime.date(1441, 3, 19), datetime.date(1444, 3, 3), "common"),
                  Era("文安", "Bunnann", datetime.date(1444, 3, 3), datetime.date(1449, 8, 25), "common"),
                  Era("宝徳", "Houtoku", datetime.date(1449, 8, 25), datetime.date(1452, 8, 19), "common"),
                  Era("享徳", "Kyoutoku", datetime.date(1452, 8, 19), datetime.date(1455, 9, 15), "common"),
                  Era("康正", "Koushou", datetime.date(1455, 9, 15), datetime.date(1457, 10, 25), "common"),
                  Era("長禄", "Chouroku", datetime.date(1457, 10, 25), datetime.date(1461, 2, 10), "common"),
                  Era("寛正", "Kannshou", datetime.date(1461, 2, 10), datetime.date(1466, 3, 23), "common"),
                  Era("文正", "Bunnshou", datetime.date(1466, 3, 23), datetime.date(1467, 4, 18), "common"),
                  Era("応仁", "Ouninn", datetime.date(1467, 4, 18), datetime.date(1469, 6, 17), "common"),
                  Era("文明", "Bunnmei", datetime.date(1469, 6, 17), datetime.date(1487, 8, 18), "common"),
                  Era("長享", "Choukyou", datetime.date(1487, 8, 18), datetime.date(1489, 9, 25), "common"),
                  Era("延徳", "Entoku", datetime.date(1489, 9, 25), datetime.date(1492, 8, 21), "common"),
                  Era("明応", "Meiou", datetime.date(1492, 8, 21), datetime.date(1501, 3, 28), "common"),
                  Era("文亀", "Bunnki", datetime.date(1501, 3, 28), datetime.date(1504, 3, 26), "common"),
                  Era("永正", "Eishou", datetime.date(1504, 3, 26), datetime.date(1521, 10, 3), "common"),
                  Era("大永", "Daiei", datetime.date(1521, 10, 3), datetime.date(1528, 9, 13), "common"),
                  Era("享禄", "Kyouroku", datetime.date(1528, 9, 13), datetime.date(1532, 9, 8), "common"),
                  Era("天文", "Tennbunn", datetime.date(1532, 9, 8), datetime.date(1555, 11, 17), "common"),
                  Era("弘治", "Kouji", datetime.date(1555, 11, 17), datetime.date(1558, 3, 28), "common"),
                  Era("永禄", "Eiroku", datetime.date(1558, 3, 28), datetime.date(1570, 6, 6), "common"),
                  Era("元亀", "Gennki", datetime.date(1570, 6, 6), datetime.date(1573, 9, 4), "common"),
                  Era("天正", "Tennshou", datetime.date(1573, 9, 4), datetime.date(1593, 1, 10), "common"),
                  Era("文禄", "Bunnroku", datetime.date(1593, 1, 10), datetime.date(1596, 12, 16), "common"),
                  Era("慶長", "Keichou", datetime.date(1596, 12, 16), datetime.date(1615, 9, 5), "common"),
                  Era("元和", "Genna", datetime.date(1615, 9, 5), datetime.date(1624, 4, 17), "common"),
                  Era("寛永", "Kannei", datetime.date(1624, 4, 17), datetime.date(1645, 1, 13), "common"),
                  Era("正保", "Syouhou", datetime.date(1645, 1, 13), datetime.date(1648, 4, 7), "common"),
                  Era("慶安", "Keian", datetime.date(1648, 4, 7), datetime.date(1652, 10, 20), "common"),
                  Era("承応", "Jouou", datetime.date(1652, 10, 20), datetime.date(1655, 5, 18), "common"),
                  Era("明暦", "Meireki", datetime.date(1655, 5, 18), datetime.date(1658, 8, 21), "common"),
                  Era("万治", "Manji", datetime.date(1658, 8, 21), datetime.date(1661, 5, 23), "common"),
                  Era("寛文", "Kannbunn", datetime.date(1661, 5, 23), datetime.date(1673, 10, 30), "common"),
                  Era("延宝", "Empou", datetime.date(1673, 10, 30), datetime.date(1681, 11, 9), "common"),
                  Era("天和", "Tenna", datetime.date(1681, 11, 9), datetime.date(1684, 4, 5), "common"),
                  Era("貞享", "Joukyou", datetime.date(1684, 4, 5), datetime.date(1688, 10, 23), "common"),
                  Era("元禄", "Genroku", datetime.date(1688, 10, 23), datetime.date(1704, 4, 16), "common"),
                  Era("宝永", "Houei", datetime.date(1704, 4, 16), datetime.date(1711, 6, 11), "common"),
                  Era("正徳", "Syoutoku", datetime.date(1711, 6, 11), datetime.date(1716, 8, 9), "common"),
                  Era("享保", "Kyouhou", datetime.date(1716, 8, 9), datetime.date(1736, 6, 7), "common"),
                  Era("元文", "Gennbunn", datetime.date(1736, 6, 7), datetime.date(1741, 4, 12), "common"),
                  Era("寛保", "Kampou", datetime.date(1741, 4, 12), datetime.date(1744, 4, 3), "common"),
                  Era("延享", "Enkyou", datetime.date(1744, 4, 3), datetime.date(1748, 8, 5), "common"),
                  Era("寛延", "Kannenn", datetime.date(1748, 8, 5), datetime.date(1751, 12, 14), "common"),
                  Era("宝暦", "Houreki", datetime.date(1751, 12, 14), datetime.date(1764, 6, 30), "common"),
                  Era("明和", "Meiwa", datetime.date(1764, 6, 30), datetime.date(1772, 12, 10), "common"),
                  Era("安永", "Annei", datetime.date(1772, 12, 10), datetime.date(1781, 4, 25), "common"),
                  Era("天明", "Tennmei", datetime.date(1781, 4, 25), datetime.date(1789, 2, 19), "common"),
                  Era("寛政", "Kannsei", datetime.date(1789, 2, 19), datetime.date(1801, 3, 19), "common"),
                  Era("享和", "Kyouwa", datetime.date(1801, 3, 19), datetime.date(1804, 3, 22), "common"),
                  Era("文化", "Bunnka", datetime.date(1804, 3, 22), datetime.date(1818, 5, 26), "common"),
                  Era("文政", "Bunnsei", datetime.date(1818, 5, 26), datetime.date(1831, 1, 23), "common"),
                  Era("天保", "Tenmpou", datetime.date(1831, 1, 23), datetime.date(1845, 1, 9), "common"),
                  Era("弘化", "Kouka", datetime.date(1845, 1, 9), datetime.date(1848, 4, 1), "common"),
                  Era("嘉永", "Kaei", datetime.date(1848, 4, 1), datetime.date(1855, 1, 15), "common"),
                  Era("安政", "Ansei", datetime.date(1855, 1, 15), datetime.date(1860, 4, 8), "common"),
                  Era("万延", "Mannei", datetime.date(1860, 4, 8), datetime.date(1861, 3, 29), "common"),
                  Era("文久", "Bunnkyuu", datetime.date(1861, 3, 29), datetime.date(1864, 3, 27), "common"),
                  Era("元治", "Genji", datetime.date(1864, 3, 27), datetime.date(1865, 5, 1), "common"),
                  Era("慶応", "Keiou", datetime.date(1865, 5, 1), datetime.date(1868, 10, 23), "common"),
                  Era("明治", "Meiji", datetime.date(1868, 1, 23), datetime.date(1912, 7, 30), "common"),
                  Era("大正", "Taishou", datetime.date(1912, 7, 30), datetime.date(1926, 12, 25), "common"),
                  Era("昭和", "Shouwa", datetime.date(1926, 12, 25), datetime.date(1989, 1, 8), "common"),
                  Era("平成", "Heisei", datetime.date(1989, 1, 8), datetime.date(2019, 5, 1), "common"),
                  Era("令和", "Reiwa", datetime.date(2019, 5, 1), None, "common")
                  ]

    era_daikakuji = [Era("元徳", "Gentoku", datetime.date(1329, 9, 30), datetime.date(1331, 9, 19), "daikakuji"),
                     Era("元弘", "Genkou", datetime.date(1331, 9, 19), datetime.date(1334, 3, 13), "daikakuji"),
                     Era("建武", "Kenmu", datetime.date(1334, 3, 13), datetime.date(1336, 4, 19), "daikakuji"),
                     Era("延元", "Engen", datetime.date(1336, 4, 19), datetime.date(1340, 6, 2), "daikakuji"),
                     Era("興国", "Koukoku", datetime.date(1340, 6, 2), datetime.date(1347, 1, 28), "daikakuji"),
                     Era("正平", "Syouhei", datetime.date(1347, 1, 28), datetime.date(1370, 8, 24), "daikakuji"),
                     Era("建徳", "Kentoku", datetime.date(1370, 8, 24), datetime.date(1372, 5, 9), "daikakuji"),
                     Era("文中", "Bunchuu", datetime.date(1372, 5, 9), datetime.date(1375, 7, 4), "daikakuji"),
                     Era("天授", "Tenju", datetime.date(1375, 7, 4), datetime.date(1381, 3, 14), "daikakuji"),
                     Era("弘和", "Kouwa", datetime.date(1381, 3, 14), datetime.date(1384, 5, 26), "daikakuji"),
                     Era("元中", "Genchuu", datetime.date(1384, 5, 26), datetime.date(1392, 11, 27), "daikakuji")
                     ]

    era_jimyouin = [Era("元徳", "Gentoku", datetime.date(1329, 9, 30), datetime.date(1332, 5, 31), "jimyouin"),
                    Era("正慶", "Shoukyou", datetime.date(1332, 5, 31), datetime.date(1333, 7, 15), "jimyouin"),
                    Era("建武", "Kenmu", datetime.date(1334, 3, 13), datetime.date(1338, 10, 19), "jimyouin"),
                    Era("暦応", "Ryakuou", datetime.date(1338, 10, 19), datetime.date(1342, 6, 9), "jimyouin"),
                    Era("康永", "Kouei", datetime.date(1342, 6, 9), datetime.date(1345, 11, 23), "jimyouin"),
                    Era("貞和", "Jouwa", datetime.date(1345, 11, 23), datetime.date(1350, 4, 12), "jimyouin"),
                    Era("観応", "Kannou", datetime.date(1350, 4, 12), datetime.date(1352, 11, 12), "jimyouin"),
                    Era("文和", "Bunna", datetime.date(1352, 11, 12), datetime.date(1356, 5, 7), "jimyouin"),
                    Era("延文", "Enbun", datetime.date(1356, 5, 7), datetime.date(1361, 5, 12), "jimyouin"),
                    Era("康安", "Kouan", datetime.date(1361, 5, 12), datetime.date(1362, 10, 19), "jimyouin"),
                    Era("貞治", "Jouji", datetime.date(1362, 10, 19), datetime.date(1368, 3, 15), "jimyouin"),
                    Era("応安", "Ouan", datetime.date(1368, 3, 15), datetime.date(1375, 4, 6), "jimyouin"),
                    Era("永和", "Eiwa", datetime.date(1375, 4, 6), datetime.date(1379, 4, 17), "jimyouin"),
                    Era("康暦", "Kouryaku", datetime.date(1379, 4, 17), datetime.date(1381, 3, 28), "jimyouin"),
                    Era("永徳", "Eitoku", datetime.date(1381, 3, 28), datetime.date(1384, 3, 27), "jimyouin"),
                    Era("至徳", "Sitoku", datetime.date(1384, 3, 27), datetime.date(1387, 10, 13), "jimyouin"),
                    Era("嘉慶", "Kakyou", datetime.date(1387, 10, 13), datetime.date(1389, 3, 15), "jimyouin"),
                    Era("康応", "Kouou", datetime.date(1389, 3, 15), datetime.date(1389, 3, 15), "jimyouin"),
                    Era("明徳", "Meitoku", datetime.date(1390, 4, 20), datetime.date(1394, 8, 10), "jimyouin")
                    ]

    christ_ad = Era("西暦", "Seireki", datetime.date(1, 1, 1), None, "christian")

    era_common_daikakuji = sorted(era_common + era_daikakuji)
    era_common_jimyouin = sorted(era_common + era_jimyouin)

    def __init__(self, primary="daikakuji"):
        if primary not in {"daikakuji", "jimyouin"}:
            raise ValueError("only 'daikakuji' or 'jimyouin' are acceptable for argument 'primary'")
        self.primary = primary

    def era(self, dt, use_chris=True):
        """
        Returns one matched japanera.Era object with considering self.primary
        if use_chris, return
        """
        if self.primary == "daikakuji":
            ind = bisect_right(self.era_common_daikakuji, dt)
            if ind == 0:
                if use_chris:
                    return self.christ_ad
                return None
            if self.era_common_daikakuji[ind - 1]._in(dt):
                return self.era_common_daikakuji[ind - 1]
            if use_chris:
                return self.christ_ad
            return None
        else:
            ind = bisect_right(self.era_common_jimyouin, dt)
            if ind == 0:
                if use_chris:
                    return self.christ_ad
                return None
            if self.era_common_jimyouin[ind - 1]._in(dt):
                return self.era_common_jimyouin[ind - 1]
            if use_chris:
                return self.christ_ad
            return None

    def era_match(self, value, key=lambda x: x, cmp=lambda x, y: x._in(y), error="warn"):
        """
        Return all Era objects stored in self.era_common or self.era_daikakuji or self.era_jimyouin which
        cmp(key(Era), value) is True.
        if key is not provided, key is lambda x: x
        if cmp is not provided, cmp is lambda x, y: x._in(y)

        error sets error level
            "ignore": ignore all errors occurred while running compare
            "warn": just warn error - default
            "raise": raise any errors

        Default, this will return eras which contains given value(which must be datetime.date) in them.
        """
        eras = []
        for era in self.era_common + self.era_daikakuji + self.era_jimyouin:
            try:
                if cmp(key(era), value):
                    eras.append(era)
            except Exception:
                if error == "warn":
                    warn("There was error running cmp(key(Era), value) but skipped because ignore_error=True")
                elif error == "raise":
                    raise
        return eras

    def strftime(self, dt, fmt, _type=None, allow_before=False, use_chris=True):
        """
        %-E: Kanji era name
        %-e: Alphabet era name vowel shortened
        %-A: Alphabet era name
        %-a: First letter of alphabet era name
        %-o: Two digit year of corresponding era
        %-O: Two digit year of corresponding era. But return "元" for the first year
        %-ko: Two digit year of corresponding era in Kanji
        %-kO: Two digit year of corresponding era in Kanji. But return "元" for the first year
        %-km: Month of date in Kanji
        %-kd: Day of date in Kanji
        + datetime.strftime's format

        allow_before: object can be converted to bool. If it's True and the given dt if before than self,start,
                     %-o and %-O will be "Unknown". If False, raise an ValueError Default: False
        use_chris: bool, If True, use self.christ_ad if there is no japanera.Era match
        """
        if not _type:
            era = self.era(dt, use_chris)
        elif _type == "daikakuji":
            era = self.daikaku_era(dt, use_chris)
        elif _type == "jimyouin":
            era = self.jimyouin_era(dt, use_chris)
        else:
            raise ValueError("_type must be 'daikakuji' or 'jimyouin'")
        return era.strftime(dt, fmt, allow_before)

    def strptime(self, _str, fmt):
        """
        %-E: Kanji era name
        %-e: Alphabet era name vowel shortened
        %-A: Alphabet era name
        %-a: First letter of alphabet era name
        %-o: Two digit year of corresponding era
        %-O: Two digit year of corresponding era. But return "元" for the first year
        %-ko: Two digit year of corresponding era in Kanji
        %-kO: Two digit year of corresponding era in Kanji. But return "元" for the first year
        %-km: Month of date in Kanji
        %-kd: Day of date in Kanji
        + datetime.strftime's format
        """
        eras = self.era_common + self.era_jimyouin + self.era_daikakuji + [self.christ_ad]
        result = []
        for era in eras:
            __str, _fmt = _str, fmt

            try:
                for key in (era.kanji, era.english, era.english[0], era.english_shorten_vowel):
                    if key in __str:
                        break
                else:
                    continue
            except TypeError:
                for key in ("不明", "Unknown", "U", "Unknown"):
                    if key in __str:
                        break
                else:
                    continue

            try:
                rep = {"%-E": era.kanji, "%-A": era.english, "%-a": era.english[0],
                       "%-s": era.english_shorten_vowel, "%-o": "%y", "%-O": "%y", "%-ko": "%y", "%-kO": "%y",
                       "%-km": "%m", "%-kd": "%d",
                       }
            except TypeError:
                rep = {"%-E": "不明", "%-A": "Unknown", "%-a": "U", "%-s": "Unknown", "%-o": "%y", "%-O": "%y",
                       "%-ko": "%y", "%-kO": "%y", "%-km": "%m", "%-kd": "%d"}

            kanjis = re.compile("[一二三四五六七八九十百千万億兆京垓𥝱]+").findall(__str)
            int_from_kanji = [*map(lambda x: str(kanji2int(x)).zfill(2), kanjis)]

            if "%-O" in fmt or "%-kO" in fmt:
                _fmt = _fmt.replace("元", "01")
                __str = __str.replace("元", "01")

            for k, i in zip(kanjis, int_from_kanji):
                __str = __str.replace(k, str(i))
                _fmt = _fmt.replace(k, str(i))

            rep = dict((re.escape(k), str(v)) for k, v in rep.items())
            pattern = re.compile("|".join(rep.keys()))
            _fmt = pattern.sub(lambda m: rep[re.escape(m.group(0))], _fmt)

            try:
                tt, fraction, gmtoff_fraction = _strptime(__str, _fmt)
                time_ = list(tt[:5])
                if "%y" in _fmt:
                    time_[0] = era.start.year + time_[0] % 100 - 1
                dt = datetime.datetime(*time_)
            except ValueError:
                continue

            result.append(dt)
        return result

    def daikaku_era(self, dt, use_chris=True):
        ind = bisect_right(self.era_common_daikakuji, dt)
        if ind == 0:
            if use_chris:
                return self.christ_ad
            return None
        if self.era_common_daikakuji[ind - 1]._in(dt):
            return self.era_common_daikakuji[ind - 1]
        if use_chris:
            return self.christ_ad
        return None

    def jimyouin_era(self, dt, use_chris=True):
        ind = bisect_right(self.era_common_jimyouin, dt)
        if ind == 0:
            if use_chris:
                return self.christ_ad
            return None
        if self.era_common_jimyouin[ind - 1]._in(dt):
            return self.era_common_jimyouin[ind - 1]
        if use_chris:
            return self.christ_ad
        return None
