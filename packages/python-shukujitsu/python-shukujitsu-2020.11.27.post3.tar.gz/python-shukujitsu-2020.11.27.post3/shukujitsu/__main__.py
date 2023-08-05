
from argparse import ArgumentParser
from argparse import RawTextHelpFormatter
from sys import argv
from sys import exit
from sys import stderr

import shukujitsu


VERSION = """\
%(prog)s v{version}

MIT license <https://opensource.org/licenses/MIT>
This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.

Written by Youhei Sakurai and others; see
<https://github.com/sakurai-youhei/python-shukujitsu/graphs/contributors>.
""".format(version=shukujitsu.__version__)


def getargs(args):
    jp_holidays = shukujitsu.Japan()
    parser = ArgumentParser(prog="shukujitsu",
                            formatter_class=RawTextHelpFormatter,
                            description="Utility to match Japanese holidays "
                            "from the year %d to %d" % (min(jp_holidays).year,
                                                        max(jp_holidays).year),
                            epilog="Exit status stays 0 if one or more dates "
                            "are matched. Otherwise, it always goes 1.")
    parser.add_argument("-i", "--invert-match", action="store_true",
                        help="select non-matching dates")
    parser.add_argument("-n", "--holiday-name", action="store_true",
                        help="output holiday name instead")
    parser.add_argument("-V", "--version", action="version", version=VERSION,
                        help="display version information and exit")
    parser.add_argument("dates", metavar="DATE", type=str, nargs="*",
                        help="date to be matched")
    return parser.parse_args(args)


def main():
    args = getargs(argv[1:])
    status = 1
    try:
        if args.invert_match and args.holiday_name:
            raise RuntimeError("Both options can't be enabled, --invert-match "
                               "and --holiday-name.")
        jp_holidays = shukujitsu.Japan()
        for date in args.dates and args.dates or iter(input, None):
            try:
                key = int(date)
            except ValueError:
                key = date
            if args.invert_match:
                if key not in jp_holidays:
                    print(date.strip())
                    status = 0
            elif key in jp_holidays:
                if args.holiday_name:
                    print(jp_holidays[key])
                else:
                    print(date.strip())
                status = 0
    except (EOFError, KeyboardInterrupt):
        pass
    except Exception as e:
        print(e, file=stderr)
    finally:
        exit(status)


if __name__ == "__main__":
    main()
