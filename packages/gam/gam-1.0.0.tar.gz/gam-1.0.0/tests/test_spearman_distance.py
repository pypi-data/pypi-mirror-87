from gam.spearman_distance  import pairwise_spearman_distance_matrix
from gam.spearman_distance import (spearman_squared_distance,
                                   spearman_squared_distance_legacy)
import numpy as np


def test_spearman_symmetry():
    """Checks symmetry holds for distance metric"""
    r1 = np.array([0.1, 0.2, 0.7])
    r2 = np.array([0.6, 0.1, 0.3])
    assert spearman_squared_distance(r1, r1) == 0

    d1 = spearman_squared_distance(r1, r2)
    d2 = spearman_squared_distance(r2, r1)
    assert d1 == d2


def test_spearman_relative_distances():
    """Compares relative distances of weighted rankings"""
    r1 = np.array([0.05, 0.2, 0.7, 0.05])
    r2 = np.array([0.23, 0.24, 0.26, 0.27])
    r3 = np.array([0.22, 0.24, 0.26, 0.28])
    # r2 and r3 should be closer than r2 to r1
    assert spearman_squared_distance(r2, r3) < spearman_squared_distance(r2, r1)


# pairwise_spearman_distance_matrix(rankings)
def test_pairwise_distance_matrix():
    r1 = np.array([0.05, 0.2, 0.7, 0.05])
    r2 = np.array([0.23, 0.24, 0.26, 0.27])
    r3 = np.array([0.22, 0.24, 0.26, 0.28])

    rankings = [r1, r2, r3]
    D = pairwise_spearman_distance_matrix(rankings)
    # check symmetry, within floating point rounding margin
    assert (D[0][1] - D[1][0]) < 1e-9
    # check diagonal is zero
    assert D[1][1] == 0
    assert D[2][2] == 0
    # distance between r2 and r3 is closer than r2 and r1
    assert D[1][2] < D[1][0]


def test_spearman_accuracy():
    """ Floating point accuracy test for testing faster calculation methods """
    r1 = np.array([0.27, 0.24, 0.26, 0.23])
    r2 = np.array([0.05, 0.2, 0.7, 0.05])

    d1 = spearman_squared_distance(r1, r2)
    d2 = spearman_squared_distance_legacy(r2, r1)
    print(d1)
    print(d2)
    assert d1 == 363.37999999999994
    assert d2 == 363.37999999999994
