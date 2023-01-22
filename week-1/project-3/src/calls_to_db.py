import datetime

from .db_transactions import open_db
from collections import namedtuple

Transaction = namedtuple("Trx", ["date", "amount", "type", "habits"])


def get_all_transactions():
    res = []
    with open_db() as con:
        trx = con.get_all_trx()
    for trans in trx:
        tmsp = datetime.datetime.fromtimestamp(trans[1]).strftime("%d.%m.%Y")
        amount = str(trans[2])
        _type = "Income" if trans[3] == 0 else "Outcome"
        res.append(Transaction(str(tmsp), amount, _type, trans[4].capitalize()))
    return res
