from pkgutil import get_data

# https://www8.cao.go.jp/chosei/shukujitsu/syukujitsu.csv
BIN = get_data("shukujitsu.asof20201118", "syukujitsu.csv")
if BIN:
    TXT = BIN.decode("cp932")
else:
    raise ImportError("Can't load syukujitsu.csv under {}".format(__name__))
