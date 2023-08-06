import numpy as np
import pandas as pd


def mean_returns(data: pd.DataFrame, freq=252, type="log") -> pd.DataFrame:

    if type == "pct":
        return daily_returns(data).mean() * freq
    elif type == "log":
        return daily_log_returns(data).mean() * freq
    elif type == "year":
        return data.resample("Y").last().pct_change().mean()
    else:
        return None


def cov_matrix(data: pd.DataFrame) -> pd.DataFrame:
    return (
        daily_log_returns(data)
        .cov()
        .dropna(how="all")
        .replace([np.inf, -np.inf], np.nan)
    )


def corr_matrix(data: pd.DataFrame) -> pd.DataFrame:
    return (
        daily_log_returns(data)
        .corr()
        .dropna(how="all")
        .replace([np.inf, -np.inf], np.nan)
    )


def daily_returns(data: pd.DataFrame) -> pd.DataFrame:
    """Returns DataFrame with daily returns (percentage change)
    :Input:
     :data: ``pandas.DataFrame`` with daily stock prices
    :Output:
     :ret: a ``pandas.DataFrame`` of daily percentage change of Returns
         of given stock prices.
    """
    return data.pct_change().dropna(how="all").replace([np.inf, -np.inf], np.nan)


def daily_log_returns(data: pd.DataFrame) -> pd.DataFrame:
    """
    Returns DataFrame with daily log returns
    :Input:
     :data: ``pandas.DataFrame`` with daily stock prices
    :Output:
     :ret: a ``pandas.DataFrame`` of
         log(1 + daily percentage change of Returns)
    """
    return np.log(1.0 + daily_returns(data)).dropna(how="all")


def negative_log_return(data: pd.DataFrame):
    neg_log_return = daily_log_returns(data)
    neg_log_return[neg_log_return > 0] = 0
    return neg_log_return


def volatility(data: pd.DataFrame, freq=252) -> pd.Series:
    return (
        daily_log_returns(data)
        .std()
        .apply(lambda x: x * np.sqrt(freq))
        .dropna(how="all")
        .replace([np.inf, -np.inf], np.nan)
    )


def negative_volatility(data: pd.DataFrame, freq=252) -> pd.Series:
    return (
        negative_log_return(data)
        .std()
        .apply(lambda x: x * np.sqrt(freq))
        .dropna(how="all")
        .replace([np.inf, -np.inf], np.nan)
    )
