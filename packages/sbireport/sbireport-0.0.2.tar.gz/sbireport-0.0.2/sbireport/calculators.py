import pandas as pd


def calcposition(trades: pd.DataFrame, index_field="Код ЦБ") -> pd.DataFrame:
    buys = (
        trades[trades["Вид"] == "Покупка"]
        .groupby(index_field)
        .agg(
            {
                "Количество, шт.": "sum",
                "Сумма": "sum",
                "Комиссия Брокера": "sum",
                "Комиссия Биржи": "sum",
            }
        )
    )

    buys["Сумма"] = buys["Сумма"].apply(lambda x: -x)

    sells = (
        trades[trades["Вид"] == "Продажа"]
        .groupby(index_field)
        .agg(
            {
                "Количество, шт.": "sum",
                "Сумма": "sum",
                "Комиссия Брокера": "sum",
                "Комиссия Биржи": "sum",
            }
        )
    )

    sells["Количество, шт."] = sells["Количество, шт."].apply(lambda x: -x)
    position = (
        buys.append(sells)
        .groupby(index_field)
        .agg(
            {
                "Количество, шт.": "sum",
                "Сумма": "sum",
                "Комиссия Брокера": "sum",
                "Комиссия Биржи": "sum",
            }
        )
    )

    position["Комиссия Брокера"] = position["Комиссия Брокера"].apply(lambda x: -x)
    position["Комиссия Биржи"] = position["Комиссия Биржи"].apply(lambda x: -x)

    # position = position.join(static_data, on='Код ЦБ')

    return position


def calcweight(position: pd.DataFrame) -> pd.DataFrame:
    p = position.copy(deep=True)
    p["Вес"] = p["Сумма"] / p["Сумма"].sum()

    return p
