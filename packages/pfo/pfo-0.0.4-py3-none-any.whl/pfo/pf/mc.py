import numpy as np
import pandas as pd
from tqdm import tqdm

from pfo.pf.valuations import pf_mean_returns, pf_volatility, pf_negative_volatility
from pfo.stocks.returns import cov_matrix, mean_returns, negative_volatility


def random_weights_exp(num_assets: int):
    Y = np.random.exponential(scale=0.5, size=num_assets)
    Tk = Y.sum()
    E_list = []
    for i in range(num_assets):
        Ei = Y[i] / Tk
        E_list.append(Ei)

    return np.array(E_list)


def random_weights_norm(num_assets: int):
    # U = np.random.uniform(0, 1, num_assets-1)
    U = np.random.random_sample(num_assets - 1)
    U = np.insert(U, 0, 0.0, axis=0)
    U = np.insert(U, len(U), 1.0, axis=0)
    U.sort()

    V_list = []
    vi_1 = 0
    for i in range(len(U)):
        if i > 0:
            vi = U[i] - vi_1
            V_list.append(vi)
            vi_1 = U[i]

    return np.array(V_list)


def random_weights(num_assets):
    basis = 20.0
    U = np.random.randint(basis, size=num_assets - 1)
    U = np.insert(U, 0, 0.0, axis=0)
    U = np.insert(U, len(U), basis, axis=0)
    U.sort()

    V_list = []
    vi_1 = 0
    for i in range(len(U)):
        if i > 0:
            vi = U[i] - vi_1
            V_list.append(vi)
            vi_1 = U[i]

    return np.array(V_list) / basis


def mc_random_portfolios(
    data: pd.DataFrame, risk_free_rate=0.01, num_portfolios=10000, freq=252
):
    pbar = tqdm(total=num_portfolios)

    pf_ret = []  # Define an empty array for pf returns
    pf_vol = []  # Define an empty array for pf volatility
    pf_down_vol = []  # Define an empty array for pf downside volatility
    pf_weights = []  # Define an empty array for asset weights
    pf_sharp_ratio = []  # Define an empty array for Sharp ratio
    pf_sortino_ratio = []  # Define an empty array for Sortino ratio

    cvm = cov_matrix(data)
    stocks_returns = mean_returns(data, freq=freq, type="log")
    stocks_negative_volatility = negative_volatility(data)

    num_assets = len(data.columns)

    for idx, portfolio in enumerate(range(num_portfolios)):
        # weights = np.random.random(num_assets)
        # weights = weights / np.sum(weights)

        # weights = random_weights_norm(num_assets)
        weights = random_weights_exp(num_assets)

        pf_weights.append(weights)
        # Returns are the product of individual expected returns of asset and its weights
        returns = pf_mean_returns(weights, stocks_returns)
        pf_ret.append(returns)

        volatility = pf_volatility(
            weights, cvm, freq=freq
        )  # Annual standard deviation = volatility
        pf_vol.append(volatility)

        sh_ratio = (returns - risk_free_rate) / volatility
        pf_sharp_ratio.append(sh_ratio)

        pf_stocks_yearly_downside_vol = pf_negative_volatility(
            weights=weights, stocks_yearly_downside_vol=stocks_negative_volatility
        )
        pf_down_vol.append(pf_stocks_yearly_downside_vol)

        sor_ratio = (returns - risk_free_rate) / pf_stocks_yearly_downside_vol
        pf_sortino_ratio.append(sor_ratio)

        if idx % 1000 == 0:
            pbar.update(1000)

    pbar.close()

    df_rv = {
        "Returns": pf_ret,
        "Volatility": pf_vol,
        "Down. Volatility": pf_down_vol,
        "Sharp Ratio": pf_sharp_ratio,
        "Sortino Ratio": pf_sortino_ratio,
    }

    for counter, symbol in enumerate(data.columns, start=0):
        df_rv[symbol] = [w[counter] for w in pf_weights]

    portfolios = pd.DataFrame(df_rv)

    return portfolios
