"""
distance.py

language: python
version: 3.x
author: C. Lockhart <chris@lockhartlab.org>
"""


import numpy as np


def distance(a, b):
    """
    Compute the distance between two Trajectory instances.

    Parameters
    ----------
    a, b : Trajectory
        Two trajectories. Must have same dimensions.

    Returns
    -------
    numpy.ndarray
        Distance between every frame in the trajectory.
    """

    return np.sqrt(np.sum(np.square(a.xyz - b.xyz), axis=(1, 2)))
