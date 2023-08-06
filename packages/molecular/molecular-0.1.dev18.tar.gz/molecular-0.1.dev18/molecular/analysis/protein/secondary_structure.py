"""
secondary_structure.py
written in Python3
author: C. Lockhart <chris@lockhartlab.org>
"""

from molecular.core import Quantity, Trajectory
from molecular.external import stride

from functools import partial
from glovebox import GloveBox
import numpy as np
import os
import pandas as pd


# Class to store secondary structure results
class SecondaryStructure:
    """
    Store the result of secondary structure computation through STRIDE.

    By itself, an instance of `SecondaryStructure` is not a `Quantity`. There are several options for converting an
    instance of `SecondaryStructure` to a `Quantity`.


    """

    # STRIDE secondary structure codes
    codes = ['H', 'G', 'I', 'E', 'B', 'b', 'T', 'C']

    # Initialize instance of SecondaryStructure
    def __init__(self, data):
        """
        Initialize instance of SecondaryStructure class.

        Parameters
        ----------
        data : pandas.DataFrame
            The secondary structure data from STRIDE. Contains a column for each residue_id, and contains a row for
            each observation. Element represent the secondary structure code from STRIDE.
        """

        # Type check
        if not isinstance(data, pd.DataFrame):
            raise AttributeError('must be initialized with instance of pandas DataFrame, not %s' % type(data))

        # Set instance value
        self._data = data
        self._data_condensed = None

    def __getitem__(self, item):
        data = self._data.iloc[item, :].to_frame().T
        return SecondaryStructure(data)

    # Override __repr__
    def __repr__(self):
        # return str(self._data.agg(''.join, axis=1).values)
        return self._condense_data()

    def _condense_data(self):
        if self._data_condensed is None:
            self._data_condensed = self._data.agg(''.join, axis=1)
        return self._data_condensed

    # Handle codes
    @staticmethod
    def _handle_codes(codes):
        # If codes is not defined, use the global codes
        if codes is None:
            codes = SecondaryStructure.codes

        # Convert codes to numpy array for simplicity
        codes = np.array(codes).reshape(-1)

        # Make sure that all codes are permissible
        if ~np.isin(codes, SecondaryStructure.codes).all():
            bad_codes = [code for code in codes if code not in SecondaryStructure.codes]
            raise AttributeError('bad codes %s were provided' % bad_codes)

        # Return
        return codes

    # Mean
    def mean(self, axis=None, codes=None):
        """
        Compute the average secondary structure by code for the entire protein (axis = None), each structure (axis = 0),
        or each residue (axis = 1).

        Parameters
        ----------
        axis : None or int.
            Designates if the average should be computed for the entire protein (axis = None), each structure
            (axis = 0), or each residue (axis = 1).
        codes : str
            The secondary structure codes to compute.

        Returns
        -------
        pandas.Series or pandas.DataFrame
            If axis = None, pandas.Series is returned. Otherwise, the result will be pandas.DataFrame.
        """

        # Handle codes
        codes = self._handle_codes(codes)

        #
        result = {}
        for code in codes:
            if axis in [0, 1]:
                result[code] = np.mean(self._data == code, axis=axis)
            else:
                result[code] = self.sum(axis=None, codes=[code])[code] / np.multiply(*self._data.shape)

        # If axis is not None, coerce to DataFrame; if None, make Series. Return to user
        return pd.DataFrame(result) if axis is not None else pd.Series(result)

    # Standard deviation
    def std(self, axis=None, codes=None):
        pass

    # Sum
    def sum(self, axis=None, codes=None):
        # Handle codes
        codes = self._handle_codes(codes)

        # x
        result = {}
        for code in codes:
            if axis in [0, 1]:
                result[code] = (self._data == code).sum(axis=axis)
            else:
                result[code] = (self._data == code).sum(axis=0).sum()
        return result

    # Do residues have code?
    def residues_with_code(self, code, residue_id=None):
        """
        `Quantity`

        Parameters
        ----------
        code
        residue_id

        Returns
        -------

        """

        # Handle code
        if code is None:
            raise AttributeError('code cannot be None')
        code = self._handle_codes(code)

        # Handle residue_id
        if residue_id is None:
            residue_id = self._data.columns
        residue_id = np.array(residue_id, dtype='int').reshape(-1)

        # Return as Quantity
        return Quantity(self._data[residue_id].isin(code))

    @property
    def sequence(self):
        return self._condense_data().values

    def to_csv(self, fname):
        """
        Write secondary structure object to comma-separated file.

        Parameters
        ----------
        fname

        Returns
        -------

        """

        self._data.to_csv(fname)


# Compute secondary structure using stride for a trajectory
def secondary_structure(trajectory, executable='stride', progress_bar=False):
    """
    Compute the secondary structure for :class:`molecular.Trajectory`.

    Parameters
    ----------
    trajectory : Trajectory
        An instance of Structure or Trajectory
    executable : str
        Path to stride executable. (Default: stride)
    progress_bar : bool
        Should we show a progress bar? (Default: False)

    Returns
    -------
    SecondaryStructure
        The secondary structure for the object.
    """

    # If not Trajectory, throw an error
    if not isinstance(trajectory, Trajectory):
        raise AttributeError('cannot interpret %s' % trajectory)

    # Filter only peptide atoms out of Trajectory
    peptide_trajectory = trajectory.query('peptide', only_index=False)

    # Return the result applied to the peptide as SecondaryStructure instance
    result = pd.DataFrame(peptide_trajectory.apply(partial(_compute_secondary_structure, executable=executable),
                                                   progress_bar=progress_bar))
    result['structure_id'] = np.arange(peptide_trajectory.n_structures)
    return SecondaryStructure(result.set_index('structure_id'))


# Compute the secondary structure for a single structure
def _compute_secondary_structure(structure, executable='stride'):
    """
    Compute the secondary structure for a :func:`molecular.Structure` instance

    Parameters
    ----------
    structure : Structure
        Instance of Structure class.
    executable : str
        Path to STRIDE executable.

    Returns
    -------
    pandas.Series
        The secondary structure
    """
    # Create temporary PDB in glovebox
    gb = GloveBox('molecular-stride', persist=True)
    temp_pdb = os.path.join(gb.path, 'temp.pdb')
    structure.to_pdb(temp_pdb)

    # Run STRIDE
    result = stride(temp_pdb, executable=executable)[['residue_id', 'secondary_structure']]

    # Clean out the glovebox
    gb.clean()

    # Return
    return result.set_index('residue_id').iloc[:, 0]
