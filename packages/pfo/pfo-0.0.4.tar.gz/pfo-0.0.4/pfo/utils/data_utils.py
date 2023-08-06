import pandas as pd

from pfo.utils.market_data import _price_col_names


def price_column(columns: list):
    """This function takes list of columns and returns
    preferable name for analysis i.e. Adj. Close is preferable to Close.
    Preferable colums will be extracted to config file in the future.
     :Output:
      : column name: str,
    """
    unique_names = list(set(columns))

    for name in unique_names:
        if name in _price_col_names:
            return name

    return None


def clean_data(data: pd.DataFrame) -> pd.DataFrame:
    """This function takes pandas dataframe with multindex column
    and transforms it to a simple dataframe with prices. The new
    i.e. , index = Date, columns names are stocks, values - preferable
    prices
     :Output:
      : data: pandas datafram, index = Date,
    """

    priority_column = price_column(data.columns.get_level_values(0))

    if not isinstance(data, pd.DataFrame):
        raise ValueError("data should be a pandas.DataFrame")
    elif not isinstance(data.columns, pd.MultiIndex):
        raise ValueError("Multiindex pandas.DataFrame is expected like Close/AAPL")
    elif priority_column == None:
        raise ValueError("Can not find a column with prices")

    columns = []
    for index, item in enumerate(
        data.columns.get_level_values(0), start=0
    ):  # Python indexes start at zero
        if item == priority_column:
            columns.append(index)

    data = data.iloc[:, columns]
    data.columns = data.columns.droplevel(0)
    return data
