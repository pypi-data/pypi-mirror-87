"""
transform.py

language: Python
version: 3.7
author: C. Lockhart <chris@lockhartlab.org>
"""

from numba import njit
import numpy as np


def fit(a, b, backend='python'):
    """
    `a` and `b` must be paired.

    Parameters
    ----------
    a : molecular.Trajectory
    b : molecular.Trajectory
    backend

    Returns
    -------

    """

    # Number of structures
    n_structures = a.n_structures
    if n_structures != b.n_structures:
        raise AttributeError('a and b must have the same number of structures')

    # Number of atoms
    n_atoms = a.n_atoms
    if n_atoms != b.n_atoms:
        raise AttributeError('a and b must have the same number of atoms')

    # Number of dimensions
    n_dim = 3

    # Get coordinates
    a_xyz = a.xyz
    b_xyz = b.xyz

    # Centers
    a_xyz_center = np.tile(a_xyz.mean(axis=1), n_atoms).reshape(n_structures, n_atoms, n_dim)
    b_xyz_center = np.tile(b_xyz.mean(axis=1), n_atoms).reshape(n_structures, n_atoms, n_dim)

    # Move structures to center
    # a_xyz = to_origin(a.xyz)
    # b_xyz = to_origin(b.xyz)
    a_xyz = a_xyz - a_xyz_center
    b_xyz = b_xyz - b_xyz_center

    # Transpose b
    b_xyz_transpose = np.transpose(b_xyz, axes=[0, 2, 1])

    # Compute covariance matrix
    covariance_matrix = np.matmul(b_xyz_transpose, a_xyz)

    # Get rotation matrix
    rotation_matrix = _get_rotation_matrix(covariance_matrix)

    # Perform optimal rotation
    b_xyz = np.matmul(b_xyz, rotation_matrix)

    # Move b to a center
    b_xyz = b_xyz + a_xyz_center

    # Return
    return b_xyz


def to_origin(a):
    """

    Parameters
    ----------
    a

    Returns
    -------

    """

    # Compute the center
    # TODO put this in geometry.center ?
    center = a.xyz.mean(axis=1)

    # Transform
    a.xyz = a.xyz - center

    # Return
    return a


def _fit(a_xyz, b_xyz, backend='python'):
    """
    `a_xyz` and `b_xyz` must be paired.

    Parameters
    ----------
    a_xyz : numpy.ndarray
    b_xyz : numpy.ndarray
    backend : str

    Returns
    -------

    """

    # Extract dimensions
    n_structures, n_atoms, n_dim = a_xyz.shape

    # Sanity check
    if n_structures != b_xyz.shape[0]:
        raise AttributeError('a_xyz and b_xyz must have the same number of structures')
    if n_atoms != b_xyz.shape[1]:
        raise AttributeError('a_xyz and b_xyz must have the same number of atoms')

    # Centers
    a_xyz_center = np.tile(a_xyz.mean(axis=1), n_atoms).reshape(n_structures, n_atoms, n_dim)
    b_xyz_center = np.tile(b_xyz.mean(axis=1), n_atoms).reshape(n_structures, n_atoms, n_dim)

    # Move structures to center
    a_xyz = a_xyz - a_xyz_center
    b_xyz = b_xyz - b_xyz_center

    # Transpose b
    b_xyz_transpose = np.transpose(b_xyz, axes=[0, 2, 1])

    # Compute covariance matrix
    covariance_matrix = np.matmul(b_xyz_transpose, a_xyz)

    # Get rotation matrix
    rotation_matrix = _get_rotation_matrix(covariance_matrix)

    # Perform optimal rotation
    b_xyz = np.matmul(b_xyz, rotation_matrix)

    # Move b to a center
    b_xyz = b_xyz + a_xyz_center

    # Return
    return b_xyz



@njit
def _get_rotation_matrix(covariance_matrix):
    """
    Compute the rotation matrix from the method from Kabsch (1976) Acta Cryst. A32.



    Parameters
    ----------
    covariance_matrix

    Returns
    -------

    """
    n_structures = covariance_matrix.shape[0]
    rotation_matrix = []
    for i in range(n_structures):
        u, s, v = np.linalg.svd(covariance_matrix[i, :, :], full_matrices=True)
        s = np.diag(np.array([1., 1., np.sign(np.linalg.det(np.dot(u, v)))]))
        r = np.dot(np.dot(u, s), v)
        rotation_matrix.append(r)
    return rotation_matrix
