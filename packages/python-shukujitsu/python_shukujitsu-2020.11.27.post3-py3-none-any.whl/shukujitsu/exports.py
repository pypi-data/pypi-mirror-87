from collections import ChainMap

from shukujitsu.holidays import JapaneseHolidays


def Japan(years=[]):
    holidays = JapaneseHolidays()
    if years:
        maps = (holidays._year(int(yyyy)) for yyyy in years)
        holidays = JapaneseHolidays(ChainMap(*maps))
    return holidays


def CountryHoliday(country, years=[], *args, **kwargs):
    if any(args) or any(kwargs):
        raise RuntimeError("Unsupported arguments provided, %r %r" % (args,
                                                                      kwargs))
    elif country not in "Japan JP JPN".split():
        raise RuntimeError("Unsupported country provided, %s" % country)
    return Japan(years)
