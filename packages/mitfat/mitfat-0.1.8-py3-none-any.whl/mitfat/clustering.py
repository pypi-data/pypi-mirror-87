#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 23 18:54:26 2019

@author: vbokharaie

This module includes methods of fmri_dataset class used for clustering.
"""

# %%
def cluster_scalar(X_train, no_clusters):
    """
    K-means clustering of scalara data. Scikit-learn implementation.

    Sorts the cluster such that cluser 1 always corresponds with
        the one with highest absolute mean.

    Parameters
    ----------
    X_train : numpy.ndarray
        data to be clustered. Shape is (N=1, N_voxels).
    no_clusters : int
        Number of clusters.

    Returns
    -------
    cluster_labels_sorted : numpy.ndarray
        Cluster label for each data-entry. Shape (N_voxel, 1).
    cluster_centroids_sorted : numpy.ndarray
        Centroids for each cluster.
    """
    from sklearn.cluster import KMeans

    #    assert len(X_train.shape) == 1, \
    #            print('This fucntion is to cluster scalar values for each voxel')
    #    assert np.nan not in X_train, \
    #            print('Data contain nan')
    X_train = X_train.reshape(-1, 1)
    kmeans = KMeans(n_clusters=no_clusters, random_state=0).fit(X_train)
    kmeans_labels_ = kmeans.labels_
    kmeans_centroids = kmeans.cluster_centers_

    cluster_labels_sorted, cluster_centroids_sorted = sort_cluster(
        kmeans_labels_, kmeans_centroids
    )

    cluster_labels_sorted = cluster_labels_sorted + 1

    return cluster_labels_sorted, cluster_centroids_sorted


# %%
def cluster_raw(X_train, no_clusters):
    """
    K-means clustering of time-series data.

    Sorts the cluster such that cluser 1 always corresponds with
        the one with highest absolute mean.

    Parameters
    ----------
    X_train : numpy.ndarray
        data to be clustered. Shape is (N=1, N_voxels).
    no_clusters : int
        Number of clusters.

    Returns
    -------
    cluster_labels_sorted : numpy.ndarray
        Cluster label for each data-entry. Shape is (N_voxel, 1).
    cluster_centroids_sorted : numpy.ndarray
        Centroids for each cluster. Shape is (N_time_steps, N_voxels)

    """
    import numpy as np
    from sklearn.cluster import KMeans

    X_train = X_train.T
    if np.sum(np.isnan(X_train)):
        has_nan = True
    else:
        has_nan = False

    if has_nan:
        kmeans_labels_, kmeans_centroids, kmeans_x_hat = kmeans_missing(
            X_train, no_clusters=no_clusters
        )
    else:
        kmeans = KMeans(n_clusters=no_clusters, random_state=0).fit(X_train)
        kmeans_labels_ = kmeans.labels_
        kmeans_centroids = kmeans.cluster_centers_

    cluster_labels_sorted, cluster_centroids_sorted = sort_cluster(
        kmeans_labels_, kmeans_centroids
    )
    cluster_labels_sorted = cluster_labels_sorted + 1
    return cluster_labels_sorted, cluster_centroids_sorted


# %%
def kmeans_missing(xx, no_clusters, max_iter=30):
    """
    Perform K-Means clustering on data with missing values.

    Found it in stackoverflow


    Parameters
    ----------
    xx : Numpy array
        An [n_samples, n_features] array of data to cluster.
    no_clusters : int
        Number of clusters to form..
    max_iter : int, optional
        Maximum number of EM iterations to perform.. The default is 30.

    Returns
    -------
    labels : list of int
        An [n_samples] vector of integer labels.
    centroids : Numpy array
        An [n_clusters, n_features] array of cluster centroids..
    x_hat : Numpy arra
        Copy of xx with the missing values filled in..
    """
    # dependencies
    from sklearn.cluster import KMeans
    import numpy as np

    # Initialize missing values to their column means
    prev_centroids = (
        []
    )  # just added tp remove warning that says they are used before being define
    prev_labels = (
        []
    )  # just added tp remove warning that says they are used before being define

    missing = ~np.isfinite(xx)
    mu_ = np.nanmean(xx, 0, keepdims=1)
    x_hat = np.where(missing, mu_, xx)

    for cc_ in np.arange(max_iter):
        if cc_ > 0:
            # initialize KMeans with the previous set of centroids. this is much
            # faster and makes it easier to check convergence (since labels
            # won't be permuted on every iteration), but might be more prone to
            # getting stuck in local minima.
            cls = KMeans(no_clusters, init=prev_centroids)
        else:
            # do multiple random initializations in parallel
            cls = KMeans(no_clusters, n_jobs=-1)

        # perform clustering on the filled-in data
        labels = cls.fit_predict(x_hat)
        centroids = cls.cluster_centers_

        # fill in the missing values based on their cluster centroids
        x_hat[missing] = centroids[labels][missing]

        # when the labels have stopped changing then we have converged
        if cc_ > 0 and np.all(labels == prev_labels):
            break

        prev_labels = labels
        prev_centroids = cls.cluster_centers_

    return labels, centroids, x_hat


# %%
def sort_cluster(cluster_labels, cluster_centroids):
    """
    Sort the cluster numbers.

    Sorted such that cluster 1 always correspond with centroid with highest mean absolute value.

    Parameters
    ----------
    cluster_labels : list of int
        cluster labels.
    cluster_centroids :
        cluster centroids.

    Returns
    -------
    cluster_labels_out : list of int
        sorted lable list.
    clusters_centroids_out : Numpy array
        sorted centroids.

    """
    import numpy as np

    cent_mean = np.mean(cluster_centroids, axis=1)
    cent_mean_arg_sorted = np.argsort(cent_mean)
    cent_mean_arg_sorted = cent_mean_arg_sorted[::-1]
    cent_mean_arg_sorted_SORTED = np.argsort(cent_mean_arg_sorted)

    list_cluster_labels = list(cluster_labels)

    list_cluster_labels_out = [
        cent_mean_arg_sorted_SORTED[x] for x in list_cluster_labels
    ]
    cluster_labels_out = np.array(list_cluster_labels_out)
    clusters_centroids_out = cluster_centroids[cent_mean_arg_sorted, :]
    return cluster_labels_out, clusters_centroids_out


# %%
def kmean_it(self, cluster_no):
    """
    To function as a wrapper for sklearn.cluster.KMeans.

    Sorts the clusters, assigns cluster labels to bbox non-zero cells

    Parameters
    ----------
    cluster_no : int
        cluster number..

    Returns
    -------
    bbox_cat : numpy array
        mask for voxels to consider. shape (e1, e2, e3).
    cluster_labels_sorted : list of int
        Sorted list of cluster labels.
    cluster_centroids_sorted : numpy array
        Centroids, sorted.

    """
    from sklearn.cluster import KMeans
    import numpy as np

    # clustering
    mask_bbox = self.mask
    X = self.data_normalised
    kmeans = KMeans(n_clusters=cluster_no, random_state=0).fit(X)
    cluster_labels_sorted, cluster_centroids_sorted = sort_cluster(
        kmeans.labels_, kmeans.cluster_centers_
    )
    bbox_cat = np.int8(np.zeros(np.shape(mask_bbox))) - 1
    bbox_cat[mask_bbox == 1] = cluster_labels_sorted
    return bbox_cat, cluster_labels_sorted, cluster_centroids_sorted


