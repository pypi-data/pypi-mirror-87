import numpy as np
import pandas as pd
from matplotlib import pylab as plt
from scipy.cluster.vq import vq
from sklearn.cluster import KMeans
from pfo.utils.data_utils import clean_data

from pfo.stocks.returns import mean_returns, daily_log_returns, volatility


def cluster_stocks(data: pd.DataFrame, n_clusters=5, verbose=False):
    """Gets the number of clusters and tries to cluster(KMeans) stocks based on
    the mean returns and volatility. The decision about optimal number
    of clusters can be made based on an elbow curve. Max number of cluster is
    20.
    Good article about elbow curve:
    https://blog.cambridgespark.com/how-to-determine-the-optimal-number-of-clusters-for-k-means-clustering-14f27070048f
    The function creates following plots:
     1. Elbow curve to make decision about optimal number of clusters
     2. A plot with K-Means clustered by return and volatility stocks and centroids.
     3. Plots with clusters and their daily return cumulative sum over the given period
    :Input:
         : data: ``pandas.DataFrame`` stock prices
         :n_clusters: ``int`` (default: 5), should be > 2 and less than number of stocks in
         pf
         :verbose: ``boolean`` (default= ``False``), whether to print out clusters
    :Output:
         :clusters: ``list`` of (Stocks) tickers.
    """

    if not isinstance(n_clusters, int):
        raise ValueError("Total number of clusters must be integer.")
    elif n_clusters < 2:
        raise ValueError(f"Total number of clusters({len(data.columns)}) must be > 2.")
    elif len(data.columns) < 3:
        raise ValueError(
            f"Total number of stocks in pf({len(data.columns)}) must be > 2."
        )
    elif n_clusters > len(data.columns):
        raise ValueError(
            f"Total number of clusters({n_clusters}) "
            f"must be <= number of stocks({len(data.columns)}) in pf"
        )

    if isinstance(data.columns, pd.MultiIndex):
        data = clean_data(data)

    pf_return_means = mean_returns(data, type="log")
    pf_daily_returns = daily_log_returns(data)
    pf_volatility = volatility(data)
    # format the data as a numpy array to feed into the K-Means algorithm
    data_ret_vol = np.asarray(
        [np.asarray(pf_return_means), np.asarray(pf_volatility)]
    ).T

    distorsions = []
    max_n_clusters = min(20, len(data.columns))

    for k in range(2, max_n_clusters):
        k_means = KMeans(n_clusters=k)
        k_means.fit(X=data_ret_vol)
        distorsions.append(k_means.inertia_)

    plt.plot(
        range(2, max_n_clusters),
        distorsions,
        linestyle="-",
        color="red",
        lw=2,
        label="Elbow curve",
    )
    plt.title("Elbow curve")
    plt.xlabel("Number of clusters")
    plt.ylabel("Distortion")
    plt.grid(True)
    plt.legend()

    # Step size of the mesh. Decrease to increase the quality of the VQ.
    h = 0.002  # point in the mesh [x_min, x_max]x[y_min, y_max].

    x_min, x_max = data_ret_vol[:, 0].min() - 0.1, data_ret_vol[:, 0].max() + 0.1
    y_min, y_max = data_ret_vol[:, 1].min() - 0.1, data_ret_vol[:, 1].max() + 0.1
    xx, yy = np.meshgrid(np.arange(x_min, x_max, h), np.arange(y_min, y_max, h))

    km = KMeans(n_clusters=n_clusters)
    km.fit(data_ret_vol)

    centroids = km.cluster_centers_

    # Obtain labels for each point in mesh. Use last trained model.
    Z = km.predict(np.c_[xx.ravel(), yy.ravel()]).reshape(xx.shape)

    # some plotting using numpy's logical indexing
    plt.figure(figsize=(10, 6))
    plt.imshow(
        Z,
        interpolation="nearest",
        extent=(xx.min(), xx.max(), yy.min(), yy.max()),
        cmap=plt.cm.Paired,
        aspect="auto",
        origin="lower",
    )

    # Plot the centroids as a white X
    plt.scatter(
        centroids[:, 0], centroids[:, 1], marker="*", s=420, color="white", zorder=10
    )
    # Plot stocks
    plt.plot(data_ret_vol[:, 0], data_ret_vol[:, 1], "o", markersize=12)

    plt.title("K-means clustering\n" "Centroids are marked with white star")
    plt.xlabel("Returns")
    plt.ylabel("Volatility")

    idx, _ = vq(data_ret_vol, centroids)
    clusters = {}

    for i in list(set(idx)):
        clusters[i] = []

    for name, cluster in zip(pf_return_means.index, idx):
        clusters[cluster].append(name)

    # Calculating avg comulative daily return for each cluster and store
    # in pf_daily_returns under special stock name - avg{Cluster index}
    for i in list(set(idx)):
        s = "avg" + str(i)
        pf_daily_returns[s] = pf_daily_returns[clusters[i]].mean(axis=1)

    for n in range(n_clusters):
        # plot clusters
        plt.figure(figsize=(10, 6))

        for stock in clusters[n]:
            # plot stocks as grey lines
            plt.plot(pf_daily_returns[stock].cumsum(), "gray", linewidth=1)

        plt.title(f"Cluster #{n}")
        plt.ylabel("Daily returns cumulative sum")
        # plot average to see cluster dynamic
        s = "avg" + str(n)
        plt.plot(pf_daily_returns[s].cumsum(), "red", linewidth=3)
        plt.xticks(rotation=30)
        plt.grid(True)

        if verbose:
            print(f"Cluster #{n}")
            print(clusters[n])

    return clusters
