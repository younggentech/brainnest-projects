import datetime

from .db_transactions import open_db
from collections import namedtuple

Transaction = namedtuple("Trx", ["date", "amount", "type", "habits"])


def get_all_transactions():
    results = []
    with open_db() as db:
        transactions = db.get_all_transactions()
    for transaction in transactions:
        timestamp = datetime.datetime.fromtimestamp(transaction[1]).strftime("%d.%m.%Y")
        amount = str(transaction[2])
        _type = "Income" if transaction[3] == "income" else "Outcome"
        results.append(Transaction(str(timestamp), amount, _type, str(transaction[4]).capitalize()))
    return results
