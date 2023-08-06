import numpy as np


def pf_variance(weights, cov_matrix):
    return cov_matrix.mul(weights, axis=0).mul(weights, axis=1).sum().sum()


def pf_daily_returns(weights, daily_returns):
    return weights * daily_returns


def pf_mean_returns(weights, yearly_returns):
    return np.dot(weights, yearly_returns)


def pf_volatility(weights, pf_cvm, freq=252):
    var = pf_variance(weights, pf_cvm)  # Portfolio Variance
    daily_volatility = np.sqrt(var)  # Daily standard deviation
    return daily_volatility * np.sqrt(freq)  # Annual standard deviation = volatility


def pf_negative_volatility(weights, stocks_yearly_downside_vol):
    return (stocks_yearly_downside_vol * weights).sum()
