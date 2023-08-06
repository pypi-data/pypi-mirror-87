import datetime

import apimoex
import pandas as pd
import requests
from tqdm import tqdm


def get_board_tickers(board={"board": "TQBR", "shares": "shares"}):
    """This function returns list with tickers available on a specific board.
    :Input:
     :board : dict like {'board': 'TQBR', 'shares': 'shares'},
    :Output:
     : tickers - list
    """
    arguments = {"securities.columns": ("SECID," "REGNUMBER," "LOTSIZE," "SHORTNAME")}
    brd = board.get("board")
    shares = board.get("shares")
    request_url = (
        "https://iss.moex.com/iss/engines/stock/"
        f"markets/{shares}/boards/{brd}/securities.json"
    )

    with requests.Session() as session:
        iss = apimoex.ISSClient(session, request_url, arguments)
        iis_data = iss.get()
        board_df = pd.DataFrame(iis_data["securities"])
        board_df.set_index("SECID", inplace=True)

    return board_df.index.tolist()


def _download_moex(
    tickers: list, start_date: datetime, end_date: datetime, boards: list
) -> pd.DataFrame:

    data = pd.DataFrame()
    arguments = {"securities.columns": ("SECID," "REGNUMBER," "LOTSIZE," "SHORTNAME")}
    for board in boards:
        board_tickers = []
        brd = board.get("board")
        shares = board.get("shares")
        request_url = (
            "https://iss.moex.com/iss/engines/stock/"
            f"markets/{shares}/boards/{brd}/securities.json"
        )

        with requests.Session() as session:
            iss = apimoex.ISSClient(session, request_url, arguments)
            iis_data = iss.get()
            board_df = pd.DataFrame(iis_data["securities"])
            board_df.set_index("SECID", inplace=True)

            columns = ["TRADEDATE", "WAPRICE", "CLOSE"]
            stocks_prices = []
            if len(tickers) == 0:
                board_tickers = board_df.index.tolist()
            else:
                board_tickers = tickers

            pbar = tqdm(total=len(board_df.index))
            for stock in board_df.index:
                if stock in board_tickers:
                    stock_data = apimoex.get_board_history(
                        session=session,
                        security=stock,
                        start=start_date,
                        end=end_date,
                        columns=columns,
                        market=shares,
                        board=brd,
                    )
                    stock_df = pd.DataFrame(stock_data)
                    stock_df["TRADEDATE"] = pd.to_datetime(stock_df["TRADEDATE"])
                    stock_df.set_index("TRADEDATE", inplace=True)
                    stock_df = pd.concat([stock_df], axis=1, keys=[stock]).swaplevel(
                        0, 1, 1
                    )
                    stocks_prices.append(stock_df)

                pbar.update(1)
            pbar.clear()

            if len(stocks_prices) > 0:
                data1 = pd.concat(stocks_prices, join="outer", axis=1)
                if len(data.columns) == 0:
                    data = data1.copy(deep=True)
                else:
                    data = pd.concat([data, data1], join="outer", axis=1)

    pbar.close()

    return data[start_date:end_date]
