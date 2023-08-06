"""
rmsd.py
written in Python3
author: C. Lockhart

>>> from molecular import read_pdb, rmsd
>>> trajectory = read_pdb('trajectory1.pdb')
>>> first_structure = trajectory[0]
>>> rmsd = rmsd(trajectory, first_structure)

"""

# noinspection PyProtectedMember
from molecular.transform.transform import _fit
from itertools import product
import numpy as np


# Compute the RMSD between 2 trajectories
def rmsd(a, b=None, paired=False, fit=True):
    """
    Compute the RMSD.

    If only `a` is provided, then the RMSD is computed between all structures in the Trajectory.
    Otherwise, if `a` and `b` are provided, we compute the RMSD between all structures in `a` and all structures in `b`.


    Parameters
    ----------
    a : molecular.Trajectory
    b : molecular.Trajectory
    paired : bool
        Are a and b paired? That is, should we compute RMSD between (a[0], b[0]), (a[1], b[1]), etc.? (Default: False)
    fit : bool
        Should structures be fit before RMSD is computed? (Default: True)

    Returns
    -------


    See Also
    --------
    http://manual.gromacs.org/documentation/current/onlinehelp/gmx-rms.html
    """

    # If a is None, then select b
    if a is None:
        b = a

    # Number of atoms between a and b must be identical
    if a.n_atoms != b.n_atoms:
        raise AttributeError('a and b must have same number of atoms')

    # Get coordinates
    a_xyz = a.xyz
    b_xyz = b.xyz

    # Compute paired?
    if paired:
        if len(a) != len(b):
            raise AttributeError('cannot compute paired RMSD because a and b have different number of structures')
        # iterable = zip(range(a.n_structures), range(b.n_structures))
        a_index = range(a.n_structures)
        b_index = range(b.n_structures)

    # Otherwise, compute RMSD taking a x b
    else:
        # FIXME the problem with this that it's memory-intensive to replicate ...
        # iterable = product(range(a.n_structures), range(b.n_structures))
        ab_product = np.array(list(product(range(a.n_structures), range(b.n_structures))))
        a_index, b_index = ab_product[:, 0], ab_product[:, 1]

    # Expand a_xyz and b_xyz so they have the same dimensions and are "paired"
    a_xyz = a_xyz[a_index, :, :]
    b_xyz = b_xyz[b_index, :, :]

    # Should we fit the two structures?
    if fit:
        b_xyz = _fit(a_xyz, b_xyz)

    # Compute the difference between a and b
    # diff = a_xyz[a_index, :, :] - b_xyz[b_index, :, :]

    # Actually Compute RMSD
    result = np.sqrt(np.sum(np.square(a_xyz - b_xyz), axis=(1, 2)) / a.n_atoms)
    # result = np.zeros((a.n_structures, b.n_structures))
    # for i, j in iterable:
    #     result[i, j] = np.sqrt(np.mean((a_xyz[i, :, :] - b_xyz[j, :, :]) ** 2))

    # Pivot into wide form
    # https://stackoverflow.com/questions/17028329/python-create-a-pivot-table
    # rows, row_pos = np.unique(a_index, return_inverse=True)
    # cols, col_pos = np.unique(b_index, return_inverse=True)
    # pivot_table = np.zeros((len(rows), len(cols)))
    # pivot_table[row_pos, col_pos] = result
    result = result.reshape(a.n_structures, b.n_structures)

    # Return
    return result

#
# def _rmsd(a, b, paired=False, fit=True):
#     """
#
#     Parameters
#     ----------
#     a
#     b
#
#     Returns
#     -------
#
#     """
#
#     # Get the number of elements in a and b
#     n_a = len(a)
#     n_b = len(b)
#
#     a_xyz = a.xyz
#     b_xyz = b.xyz
#
#     # Should we fit the two structures?
#     if fit:
#         b_xyz = _fit(a, b)
#
#     result = np.zeros((n_a, n_b))
#     if not paired:
#         iterable = product(range(n_a), range(n_b))
#     else:
#         iterable = zip(range(n_a), range(n_b))
#     for i, j in iterable:
#         result[i, j] = np.sqrt(np.mean((a_xyz[i, :, :] - b_xyz[j, :, :]) ** 2))
#
#     return result
