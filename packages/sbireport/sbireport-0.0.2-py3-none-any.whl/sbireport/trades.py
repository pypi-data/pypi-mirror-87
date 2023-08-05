from pathlib import Path
import pandas as pd
from bs4 import BeautifulSoup


def extract_trades(rpts_path: str) -> pd.DataFrame:
    """The function scans the folder and aggregates all html reports into
    one output. Duplicating (from trade id perspective) trades are ignored.
    :Input:
      :rpts_path: ``str``, path to folder with html reports.
    :Output:
      :trades: pandas.DataFrame with trades
    """
    p = Path(rpts_path)

    if not p.exists():
        raise Exception(f"File or folder {rpts_path} does not exist")

    files = []
    if p.is_dir():
        files = p.glob("*.html")
    else:
        files = [rpts_path]

    reports = {}
    alltrades = []
    trdids = []

    for f in files:
        soup = BeautifulSoup(open(f, encoding="utf-8"), "html.parser")
        tables = []
        # К сожалению надо перебрать все таблицы
        for tbl in soup.find_all("table"):
            output_rows = []
            for table_row in tbl.findAll("tr"):
                columns = table_row.findAll("td")
                output_row = []
                for column in columns:
                    output_row.append(column.text)
                output_rows.append(output_row)
            tables.append(output_rows)

        reports[f] = tables

    for f in reports.keys():
        tables = reports[f]
        for tbl in tables:
            if tbl[0][0] == "Дата заключения":
                for row in tbl:
                    if (
                        row[0]
                        not in [
                            "Итого, RUB",
                            "Дата заключения",
                            "Площадка: Фондовый рынок",
                        ]
                        and row[13] not in trdids
                    ):
                        alltrades.append(row)
                        trdids.append(row[13])

    trades = pd.DataFrame(
        alltrades,
        columns=[
            "Дата заключения",
            "Дата расчетов",
            "Время заключения",
            "Наименование ЦБ",
            "Код ЦБ",
            "Валюта",
            "Вид",
            "Количество, шт.",
            "Цена",
            "Сумма",
            "НКД",
            "Комиссия Брокера",
            "Комиссия Биржи",
            "Номер сделки",
            "Комментарий",
            "Статус сделки",
        ],
    )
    trades[["Дата заключения", "Дата расчетов"]] = trades[
        ["Дата заключения", "Дата расчетов"]
    ].apply(pd.to_datetime)
    trades[
        [
            "Количество, шт.",
            "Цена",
            "Сумма",
            "НКД",
            "Комиссия Брокера",
            "Комиссия Биржи",
        ]
    ] = trades[
        [
            "Количество, шт.",
            "Цена",
            "Сумма",
            "НКД",
            "Комиссия Брокера",
            "Комиссия Биржи",
        ]
    ].apply(
        lambda x: pd.to_numeric(x.astype(str).str.replace(" ", ""), errors="coerce")
    )

    return trades
