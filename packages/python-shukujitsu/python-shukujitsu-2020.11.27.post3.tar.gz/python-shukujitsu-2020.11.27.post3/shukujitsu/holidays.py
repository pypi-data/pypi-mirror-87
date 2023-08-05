from collections import UserDict
from csv import reader
from datetime import date
from datetime import datetime
from datetime import timedelta

from dateutil.parser import parse

from shukujitsu.data import load_txt


class JapaneseHolidays(UserDict):
    def __init__(self, *args, **kwargs):
        if args or kwargs:
            super().__init__(*args, **kwargs)
        else:
            csv = reader(load_txt().splitlines())
            next(csv)  # skip header
            super().__init__({date(*map(int, holiday.split("/"))): name
                              for holiday, name in csv})

    def __str__(self):
        return "<JapaneseHolidays %d days from %d to %d>" % (
            len(self), min(self).year, max(self).year)

    def __keytransform__(self, key):
        if isinstance(key, datetime):
            return key.date()
        elif isinstance(key, date):
            return key
        elif isinstance(key, (int, float)):
            return datetime.utcfromtimestamp(key).date()
        elif isinstance(key, str):
            try:
                return parse(key).date()
            except (ValueError, OverflowError):
                raise ValueError("Cannot parse date from string '%s'" % key)
        else:
            raise TypeError("Cannot convert type '%s' to date." % type(key))

    def __contains__(self, key):
        return super().__contains__(self.__keytransform__(key))

    def __getitem__(self, key):
        if isinstance(key, slice):
            return list(self._slice(*self._unpack(key)))
        else:
            return super().__getitem__(self.__keytransform__(key))

    def _unpack(self, slice_):
        if slice_.step is None:
            step = 1
        elif isinstance(slice_.step, timedelta):
            step = slice_.step.days
        elif isinstance(slice_.step, int):
            step = slice_.step
        else:
            raise TypeError("Cannot convert type '%s' to int." % type(step))

        if step == 0:
            raise ValueError('Step value must not be zero.')
        elif not slice_.start or not slice_.stop:
            raise ValueError("Both start and stop must be given.")
        else:
            start = self.__keytransform__(slice_.start)
            stop = self.__keytransform__(slice_.stop)
            return start, stop, step

    def _slice(self, start, stop, step):
        for delta in range(0, (stop - start).days, step):
            day = start + timedelta(days=delta)
            if day in self:
                yield day

    def _year(self, yyyy):
        return type(self)({day: self[day] for day in self if day.year == yyyy})
