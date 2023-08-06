import pandas as pd
from matplotlib import pylab as plt
from pfo.utils.data_utils import clean_data
from pfo.stocks.returns import (
    mean_returns,
    volatility,
    negative_volatility,
    daily_log_returns,
)
import numpy as np


class stock(object):
    """Object that contains information about a stock.
    The class allows to show all ratios and plots required
    for analysis
    """

    def __init__(self, ticker, data: pd.DataFrame, **kwargs):
        if not isinstance(data, pd.DataFrame):
            raise ValueError("data should be a pandas.DataFrame")

        if isinstance(data.columns, pd.MultiIndex):
            self._data = clean_data(data).dropna(how="all")
        else:
            self._data = data.dropna(how="all")

        if not (ticker in self._data.columns):
            raise ValueError(f"Ticker {ticker} is not provided in DataFrame")

        self._ticker = ticker
        self._data = pd.DataFrame(self._data[ticker])

        self._risk_free_rate = kwargs.get("risk_free_rate", 0.001)
        self._freq = kwargs.get("freq", 252)
        self._type = kwargs.get("type", "log")

        self._daily_returns = daily_log_returns(self._data)

        ##########PROPERTIES##########
        self._returns = mean_returns(
            self._data, freq=self._freq, type=self._type
        ).values[0]
        self._volatility = volatility(self._data).values[0]
        self._downside_volatility = negative_volatility(self._data).values[0]
        self._sharp = (self._returns - self._risk_free_rate) / self._volatility
        self._sortino = (
            self.returns - self._risk_free_rate
        ) / self._downside_volatility
        self._skew = self._data.skew().values[0]
        self._kurtosis = self._data.kurt().values[0]

    @property
    def returns(self):
        return self._returns

    @property
    def volatility(self):

        return self._volatility

    @property
    def negative_volaitulity(self):
        return self._downside_volitility

    @property
    def sortino(self):
        return self._sortino

    @property
    def sharp(self):
        return self._sharp

    @property
    def skew(self):
        return self._skew

    @property
    def kurtosis(self):
        return self._kurtosis

    def plot_daily_returns(self):

        plt.figure(figsize=(16, 10))
        # ax = fig.add_subplot(111, projection='polar')

        plt.plot(self._daily_returns[self._ticker].cumsum(), "black", linewidth=1)
        plt.title(f"{self._ticker}")
        plt.ylabel("Daily returns cumulative sum")
        plt.xticks(rotation=30)
        plt.grid(True)

    def plot_prices(self):

        plt.figure(figsize=(16, 10))
        # ax = fig.add_subplot(111, projection='polar')

        plt.plot(self._data[self._ticker], "black", linewidth=2.0)
        plt.title(f"{self._ticker}")
        plt.ylabel("Price")
        plt.xticks(rotation=30)
        plt.grid(True)

        # Generate moving averages

        self._data["SMA5"] = self._data[self._ticker].rolling(5).mean()
        self._data["SMA20"] = self._data[self._ticker].rolling(20).mean()

        plt.plot(self._data["SMA5"], linewidth=1.0, color="red")
        plt.plot(self._data["SMA20"], linewidth=1.0, color="c")

        # Select buying and selling signals: where moving averages cross

        # Identifying the buy/sell zone
        self._data["Buy"] = np.where((self._data["SMA5"] > self._data["SMA20"]), 1, 0)
        self._data["Sell"] = np.where((self._data["SMA5"] < self._data["SMA20"]), 1, 0)

        ##identify buy sell signal
        self._data["Buy_ind"] = np.where(
            (self._data["Buy"] > self._data["Buy"].shift(1)), 1, 0
        )
        self._data["Sell_ind"] = np.where(
            (self._data["Sell"] > self._data["Sell"].shift(1)), 1, 0
        )
        ## plotting the buy and sellsignals on graph
        # plt.plot(self._data.loc[self._data['Buy_ind'] == 1])
        r = self._data.loc[self._data["Buy_ind"] == 1].index

        plt.scatter(
            self._data.loc[self._data["Buy_ind"] == 1].index,
            self._data.loc[self._data["Buy_ind"] == 1, self._ticker].values,
            label="skitscat",
            color="green",
            s=100,
            marker="^",
        )
        plt.scatter(
            self._data.loc[self._data["Sell_ind"] == 1].index,
            self._data.loc[self._data["Sell_ind"] == 1, self._ticker].values,
            label="skitscat",
            color="red",
            s=100,
            marker="v",
        )

        ## Adding labels
        plt.xlabel("Date")
        plt.ylabel("Close Price")
        plt.title(f"{self._ticker} price with buy and sell signal")

        ## plotting the buy and sellsignals on graph
