# -*- coding: utf-8 -*-

import numpy as np
import pygsp

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


def plot(G):
    if issubclass(type(G), pygsp.graphs.Graph):
        plot_graph(G)
    elif issubclass(type(G), pygsp.graphs.PointsCloud):
        plot_pointcloud(G)
    else:
        raise TypeError('Your object type is incorrect, be sure it is a PointCloud or a graphs')


def plot_graph(G):
    # TODO handling when G is a list of graphs
    # TODO integrate param when G is a clustered graph

    show_edges = G.Ne < 10000

    if show_edges:
        ki, kj = np.nonzero(G.A)
        if G.directed:
            raise NotImplementedError('TODO')
            if G.coords.shape[1] == 2:
                raise NotImplementedError('TODO')
            else:
                raise NotImplementedError('TODO')
        else:
            if G.coords.shape[1] == 2:
                fig = plt.figure()
                ax = fig.add_subplot(111)
                ki, kj = np.nonzero(G.A)
                x = np.concatenate((np.expand_dims(G.coords[ki, 0], axis=0), np.expand_dims(G.coords[kj, 0], axis=0)))
                y = np.concatenate((np.expand_dims(G.coords[ki, 1], axis=0), np.expand_dims(G.coords[kj, 1], axis=0)))
                # ax.plot(x, y, color=G.plotting['edge_color'], marker='o', markerfacecolor=G.plotting['vertex_color'])
                ax.plot(x, y, color='red', marker='o', markerfacecolor='blue')
                plt.show()
            if G.coords.shape[1] == 3:
                # Very dirty way to display a 3d graph
                fig = plt.figure()
                ax = fig.gca(projection='3d')
                x = np.concatenate((np.expand_dims(G.coords[ki, 0], axis=0), np.expand_dims(G.coords[kj, 0], axis=0)))
                y = np.concatenate((np.expand_dims(G.coords[ki, 1], axis=0), np.expand_dims(G.coords[kj, 1], axis=0)))
                z = np.concatenate((np.expand_dims(G.coords[ki, 2], axis=0), np.expand_dims(G.coords[kj, 2], axis=0)))
                ii = range(0, x.shape[1])
                x2 = np.ndarray((0, 1))
                y2 = np.ndarray((0, 1))
                z2 = np.ndarray((0, 1))
                for i in ii:
                    x2 = np.append(x2, x[:, i])
                for i in ii:
                    y2 = np.append(y2, y[:, i])
                for i in ii:
                    z2 = np.append(z2, z[:, i])
                for i in range(0, x.shape[1] * 2, 2):
                    x3 = x2[i:i + 2]
                    y3 = y2[i:i + 2]
                    z3 = z2[i:i + 2]
                    ax.plot(x3, y3, z3, color='red', marker='o', markerfacecolor='blue')
                    # ax.plot(x3, y3, z3, color=G.plotting['edge_color'], marker='o', markerfacecolor=G.plotting['vertex_color'])
                plt.show()
    else:
        if G.coords.shape[1] == 2:
            fig = plt.figure()
            ax = fig.add_subplot(111)
            ax.plot(G.coords[:, 0], G.coords[:, 1], 'bo')
            plt.show()
        if G.coords.shape[1] == 3:
            fig = plt.figure()
            ax = fig.gca(projection='3d')
            ax.plot(G.coords[:, 0], G.coords[:, 1], G.coords[:, 2], 'bo')
            plt.show()


def plot_pointcloud(P):
    r"""
    Plot the coordinates of a pointcloud.

    Parameters
    ----------
    P : PointsClouds object

    Examples
    --------
    >>> import pygsp
    >>> pygsp.graphs.dummy(0, [1, 2, 3], True)
    array([1, 2, 3])

    """
    if P.coords.shape[1] == 2:
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.plot(P.coords[:, 0], P.coords[:, 1], 'bo')
        plt.show()
    if P.coords.shape[1] == 3:
        fig = plt.figure()
        ax = fig.gca(projection='3d')
        ax.plot(P.coords[:, 0], P.coords[:, 1], P.coords[:, 2], 'bo')
        plt.show()


def plot_filter(G, filters, npoints=1000, line_width=4, x_width=3, x_size=10,
                plot_eigenvalues=None, show_sum=None):
    r"""
    Plot a system of graph spectral filters.

    Parameters
    ----------
    G : Graph object
        Description.
    filters : filter object
        Description.
    npoints : int
        Number of point where the filters are evaluated.
    line_width : int
        Width of the filters plots.
    x_width : int
        Width of the X marks representing the eigenvalues.
    x_size : int
        Size of the X marks representing the eigenvalues.
    plot_eigenvalues : boolean
        To plot black X marks at all eigenvalues of the graph (You need to \
            compute the Fourier basis to use this option). By default the \
            eigenvalues are plot if they are contained in the Graph.
    show_sum : boolean
        To plot an extra line showing the sum of the squared magnitudes\
         of the filters (default True if there is multiple filters).

    Returns
    -------
    d : ndarray
        Description.

    Examples
    --------
    >>> import pygsp
    >>> pygsp.graphs.dummy(0, [1, 2, 3], True)
    array([1, 2, 3])

    """
    if plot_eigenvalues is None:
        plot_eigenvalues = hasattr(G, 'e')
    if show_sum is None:
        show_sum = len(filters.g) > 1

    lambdas = np.linspace(0, G.lmax, npoints)

    # apply the filter
    fd = filters.evaluate(lambdas)

    # plot the filter
    size = len(fd)
    fig = plt.figure()
    ax = fig.add_subplot(111)
    if len(filters.g) == 1:
        ax.plot(lambdas, fd, linewidth=line_width)
    elif len(filters.g) > 1:
        for i in range(size):
            ax.plot(lambdas, fd[i], linewidth=line_width)

    # plot eigenvalues
    if plot_eigenvalues:
        ax.plot(G.e, np.zeros(G.N), 'xk', markeredgewidth=x_width, markersize=x_size)
    # plot highlighted eigenvalues TODO

    # plot the sum
    if show_sum:
        test_sum = np.sum(np.power(fd, 2), 0)
        ax.plot(lambdas, test_sum, 'k', linewidth=line_width)

    plt.show()


def rescale_center(x):
    r"""
    Rescaling the dataset.

    Rescaling the dataset, previously and mainly used in the SwissRoll graph.

    Parameters
    ----------
    x : ndarray
        Dataset to be rescaled.

    Returns
    -------
    r : ndarray
        Rescaled dataset.

    Examples
    --------
    >>> import pygsp
    >>> pygsp.utils.dummy(0, [1, 2, 3], True)
    array([1, 2, 3])

    """
    N = x.shape[1]
    d = x.shape[0]
    y = x - np.kron(np.ones((1, N)), np.expand_dims(np.mean(x, axis=1), axis=1))
    c = np.amax(y)
    r = y / c

    return r
