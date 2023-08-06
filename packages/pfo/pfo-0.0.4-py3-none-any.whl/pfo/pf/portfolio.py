import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy.optimize as sco

from pfo.utils.data_utils import clean_data
from pfo.pf.mc import mc_random_portfolios
from pfo.pf.valuations import pf_volatility, pf_mean_returns, pf_negative_volatility
from pfo.stocks.returns import cov_matrix, mean_returns, negative_volatility, volatility


class Portfolio(object):
    """Object that contains information about a investment pf."""

    def __init__(
        self, data: pd.DataFrame, weights=None, risk_free_rate=0.0425, freq=252
    ):
        if not isinstance(freq, int):
            raise ValueError("Frequency must be an integer")
        elif freq <= 0:
            raise ValueError("Freq must be > 0")
        else:
            self._freq = freq

        if not isinstance(risk_free_rate, (float, int)):
            raise ValueError("Risk free rate must be a float or an integer")
        else:
            self._risk_free_rate = risk_free_rate

        if not isinstance(data, pd.DataFrame):
            raise ValueError("data should be a pandas.DataFrame")

        if isinstance(data.columns, pd.MultiIndex):
            self._data = clean_data(data)
        else:
            self._data = data

        self._mc_portfolios = None
        self._mc_min_vol_port = None
        self._mc_min_downside_vol_port = None
        self._mc_max_sharpe_port = None
        self._mc_max_sortino_port = None
        self._mc_simulations_results = None
        self._weights = None
        #####################
        if weights is None:
            self._weights = np.array(
                [1.0 / len(self._data.columns) for i in range(len(self._data.columns))]
            )
        else:
            if isinstance(weights, pd.DataFrame):
                if len(weights.columns) > 1:
                    raise ValueError(
                        "Incorrect dataframe with weights provided. Expected 1 column with weights"
                    )

                weights_list = []
                for column in data.columns:
                    stock_weight = weights.at[column, weights.columns[0]]
                    weights_list.append(stock_weight)

                self._weights = np.array(weights_list)

            elif isinstance(weights, np.ndarray):
                self._weights = weights
            else:
                raise ValueError("Weights should be numpy ndarray or pd.DataFrame")

        if len(self._weights) < len(self._data.columns) or len(self._weights) > len(
            self._data.columns
        ):
            raise ValueError("Incorrect data or weights were provided")

        self._cvm = cov_matrix(self._data)
        self._mr = mean_returns(self._data, freq=self._freq)
        self._negative_vol = negative_volatility(data=self._data, freq=self._freq)

        self._df_perfomamce = {}
        self._df_perfomamce["Returns"] = self.returns
        self._df_perfomamce["Volatility"] = self.volatility
        self._df_perfomamce["Down. Volatility"] = self.negative_volatility
        self._df_perfomamce["Sharp Ratio"] = self.sharp
        self._df_perfomamce["Sortino Ratio"] = self.sortino

    @property
    def sharp(self):
        return self._sharp_ratio(self._weights)

    @property
    def sortino(self):
        return self._sortino_ratio(self._weights)

    @property
    def returns(self):
        return pf_mean_returns(self._weights, self._mr)

    @property
    def volatility(self):
        return pf_volatility(self._weights, self._cvm, freq=self._freq)

    @property
    def negative_volatility(self):
        return pf_negative_volatility(self._weights, self._negative_vol)

    ###############################################################################
    #                                     PLOT                                   #
    ###############################################################################
    def plot_mc_simulation(self):
        self._mc_portfolios.plot.scatter(
            x="Volatility",
            y="Returns",
            marker="o",
            s=10,
            alpha=0.3,
            grid=True,
            figsize=[16, 10],
        )
        plt.scatter(
            self._mc_min_vol_port[1],
            self._mc_min_vol_port[0],
            color="r",
            marker="*",
            s=500,
        )
        plt.scatter(
            self._mc_min_downside_vol_port[1],
            self._mc_min_downside_vol_port[0],
            color="c",
            marker="*",
            s=500,
        )
        plt.scatter(
            self._mc_max_sharpe_port[1],
            self._mc_max_sharpe_port[0],
            color="g",
            marker="*",
            s=500,
        )
        plt.scatter(
            self._mc_max_sortino_port[1],
            self._mc_max_sortino_port[0],
            color="y",
            marker="*",
            s=500,
        )

    def plot_stocks(self):
        """Plots the Expected annual Returns over annual Volatility of
        the stocks of the portfolio.

        """
        # annual mean returns of all stocks
        stock_returns = mean_returns(data=self._data, freq=self._freq)
        stock_volatility = volatility(data=self._data, freq=self._freq)
        # adding stocks of the portfolio to the plot
        # plot stocks individually:
        plt.scatter(stock_volatility, stock_returns, marker="o", s=100, label="Stocks")
        # adding text to stocks in plot:
        for i, txt in enumerate(stock_returns.index):
            plt.annotate(
                txt,
                (stock_volatility[i], stock_returns[i]),
                xytext=(10, 0),
                textcoords="offset points",
                label=i,
            )
            plt.legend()

    ###############################################################################
    #                                     REPORTING                               #
    ###############################################################################

    def print_mc_results(self):
        print("\n")
        print("=" * 80)
        with pd.option_context("display.max_rows", None, "display.max_columns", None):
            print(self._mc_simulations_results)
        print("=" * 80)

    def store_to_xls(self):
        pass

    def print_pf_result(self):
        print("\n")
        print("=" * 80)
        # print(self._df_perfomamce)
        print(pd.Series(self._df_perfomamce, index=self._df_perfomamce.keys()))
        print("=" * 80)

        out = {}
        for counter, ticker in enumerate(self._data.columns, start=0):
            w = np.round(self._weights[counter], 4)
            if w > 0:
                out[ticker] = w

        print(pd.Series(out, index=out.keys()))

    ###############################################################################
    #                                     SIMULATION                              #
    ###############################################################################
    def mc_simulation(self, num_portfolios=10000):
        self._mc_portfolios = mc_random_portfolios(
            data=self._data,
            risk_free_rate=self._risk_free_rate,
            num_portfolios=num_portfolios,
            freq=self._freq,
        )

        self._mc_min_vol_port = self._mc_portfolios.iloc[
            self._mc_portfolios["Volatility"].idxmin()
        ]
        self._mc_min_downside_vol_port = self._mc_portfolios.iloc[
            self._mc_portfolios["Down. Volatility"].idxmin()
        ]
        self._mc_max_sharpe_port = self._mc_portfolios.iloc[
            self._mc_portfolios["Sharp Ratio"].idxmax()
        ]
        self._mc_max_sortino_port = self._mc_portfolios.iloc[
            self._mc_portfolios["Sortino Ratio"].idxmax()
        ]
        self._mc_min_vol_port.rename_axis("Min Volatiity")
        self._mc_min_downside_vol_port.rename_axis("Down. Volatility")
        self._mc_max_sharpe_port.rename_axis("Max Sharpe Ratio")
        self._mc_max_sortino_port.rename_axis("Max Sortino Ratio")

        self._mc_simulations_results = pd.concat(
            [
                self._mc_min_vol_port,
                self._mc_min_downside_vol_port,
                self._mc_max_sharpe_port,
                self._mc_max_sortino_port,
            ],
            keys=[
                "Min Volatiity",
                "Down. Volatility",
                "Max Sharpe Ratio",
                "Max Sortino Ratio",
            ],
            join="inner",
            axis=1,
        )

    ###############################################################################
    #                                     EFFICIENT FRONTIER                      #
    ###############################################################################

    def max_sharpe_ratio(self):
        num_stocks = len(self._data.columns)
        constraints = {"type": "eq", "fun": lambda x: np.sum(x) - 1}
        bound = (0.0, 1.0)
        bounds = tuple(bound for asset in range(num_stocks))

        result = sco.minimize(
            self._neg_sharp_ratio,
            num_stocks
            * [
                1.0 / num_stocks,
            ],
            args=(),
            method="SLSQP",
            bounds=bounds,
            constraints=constraints,
        )
        return result

    def min_volatility(self):
        num_stocks = len(self._data.columns)
        cvm = cov_matrix(self._data)
        args = (cvm, self._freq)
        constraints = {"type": "eq", "fun": lambda x: np.sum(x) - 1}
        bound = (0.0, 1.0)
        bounds = tuple(bound for asset in range(num_stocks))

        result = sco.minimize(
            pf_volatility,
            num_stocks
            * [
                1.0 / num_stocks,
            ],
            args=args,
            method="SLSQP",
            bounds=bounds,
            constraints=constraints,
        )

        return result

    def efficient_return(self, target):
        num_stocks = len(self._data.columns)
        cvm = cov_matrix(self._data)

        args = (cvm, self._freq)

        def _pf_return(weights):
            ret = pf_mean_returns(weights, self._mr)
            return ret

        constraints = (
            {"type": "eq", "fun": lambda x: _pf_return(x) - target},
            {"type": "eq", "fun": lambda x: np.sum(x) - 1},
        )
        bounds = tuple((0, 1) for asset in range(num_stocks))
        result = sco.minimize(
            pf_volatility,
            num_stocks
            * [
                1.0 / num_stocks,
            ],
            args=args,
            method="SLSQP",
            bounds=bounds,
            constraints=constraints,
        )
        return result

    def efficient_frontier(self, returns_range):
        efficients = []
        for ret in returns_range:
            efficients.append(self.efficient_return(ret))
        return efficients

    def efficient_portfolios(self, plot=True):
        max_sharpe = self.max_sharpe_ratio()
        min_vol = self.min_volatility()

        returns_max_sharpe = pf_mean_returns(
            weights=max_sharpe["x"], yearly_returns=self._mr
        )
        returns_min_vol = pf_mean_returns(weights=min_vol["x"], yearly_returns=self._mr)

        target = np.linspace(returns_min_vol, returns_max_sharpe, 50)
        self._efficient_portfolios = self.efficient_frontier(returns_range=target)

        if plot:
            plt.plot(
                [p["fun"] for p in self._efficient_portfolios],
                target,
                "k-x",
                label="efficient frontier",
                color="g",
                alpha=0.3,
            )

        return self._efficient_portfolios

    def _sharp_ratio(self, weights):
        ret = pf_mean_returns(weights, self._mr)
        vol = pf_volatility(weights, self._cvm, freq=self._freq)
        return (ret - self._risk_free_rate) / vol

    def _sortino_ratio(self, weights):
        ret = pf_mean_returns(weights, self._mr)
        vol = pf_negative_volatility(weights, self._negative_vol)
        return (ret - self._risk_free_rate) / vol

    def _neg_sharp_ratio(self, weights):
        return -self._sharp_ratio(weights)

    def _neg_sortino_ratio(self, weights):
        return -self._sortino_ratio(weights)
