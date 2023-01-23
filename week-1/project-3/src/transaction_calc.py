import datetime
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.axes import SubplotBase


def read_data_from_sql(db_name="budget_db.db"):
    try:
        conn = sqlite3.connect(db_name)
        df = pd.read_sql(
            "SELECT timestamp, amount, typeOfOperation, habits FROM budget_trans", conn
        )
        return df
    finally:
        conn.close()


def create_a_bar_plot(db_name="budget_db.db", fig=None):
    df = read_data_from_sql(db_name)[["timestamp", "amount", "typeOfOperation"]]
    df["timestamp"] = df["timestamp"].apply(
        lambda x: datetime.datetime.fromtimestamp(x).strftime("%d.%m.%Y")
    )
    # df.index = df['timestamp']
    # del df['timestamp']
    if fig is None:
        fig, ax = plt.subplots(dpi=100)
    else:
        ax = fig.subplots(1)
        ax.clear()
    df["typeOfOperation"] = df["typeOfOperation"].apply(
        lambda x: "Income" if x == 0 else "Outcome"
    )
    # fig = plt.figure(figsize=(4, 3), dpi=80)
    chart = df.pivot_table(
        index=["timestamp"],
        columns=["typeOfOperation"],
        values=["amount"],
        aggfunc="sum",
    ).plot(kind="bar", rot=0, ax=ax, fontsize=5.5)
    chart.set_xlabel("")
    chart.set_ylabel("")
    chart.legend(["Income", "Outcome"])
    fig.set_figwidth(4)
    fig.set_figheight(3)
    print(fig, chart)
    return fig


if __name__ == "__main__":
    create_a_bar_plot()
