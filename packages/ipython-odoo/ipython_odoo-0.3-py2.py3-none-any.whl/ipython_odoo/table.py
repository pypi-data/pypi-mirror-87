import os

from texttable import Texttable


def tty_width():
    return os.popen('stty size', 'r').read().split()[1]


def init_table():
    table = Texttable()
    table.set_deco(Texttable.HEADER | Texttable.VLINES | Texttable.HLINES)
    table.set_max_width(tty_width())
    return table
