from fileinput import input as input_
from glob import glob as glob_
import numpy as np
import pandas as pd


# Globular loadtxt
def loadtxt(fname, dtype=float, glob=False, verbose=False):
    """
    A refactoring of :ref:`numpy.loadtxt` that allows for globbing files.

    Parameters
    ----------
    fname : file, str, or pathlib.Path
        Name of file.
    dtype : str or object
        File type.
    glob : bool
        Does `fname` need to be globbed?
    verbose : bool
        Should information about the read-in be displayed?

    Returns
    -------
    pandas.Series
        Read file
    """

    # If glob, change fname to include all globbed files
    if glob:
        # Glob first; if glob is empty, throw an error
        fname_glob = glob_(fname)
        if not fname_glob:
            raise FileNotFoundError(fname)

        # Sort glob
        fname_glob = sorted(fname_glob)

        # Output if verbose
        if verbose:
            print(f'glob: {list(fname_glob)}')

        # Update fname to include all globbed files
        fname = input_(fname_glob)

    # Utilize numpy to read-in the file(s)
    data = np.loadtxt(fname, dtype=dtype)

    # If verbose, note the shape of the data
    if verbose:
        print(f'file loaded with shape {data.shape}')

    # Return
    return data


def read_table(fname, glob=False, sep='\s+', header=None, verbose=False, **kwargs):
    """
    Read table into :class:`pandas.DataFrame`.

    Parameters
    ----------
    fname
    glob
    sep : str
    header : bool
    verbose

    Returns
    -------

    """

    # If glob, change fname to include all globbed files
    if glob:
        # Glob first; if glob is empty, throw an error
        fname_glob = glob_(fname)
        if not fname_glob:
            raise FileNotFoundError(fname)

        # Sort glob
        fnames = sorted(fname_glob)

    # Otherwise, turn fname into a list
    # TODO evaluate if creating this list is right, or if we should short-circuit the read-in
    else:
        fnames = [fname]

    # Verbose, print out files and start timer
    if verbose:
        print(f'file(s): {fnames}')
        import time
        start_time = time.time()

    # Cycle over fnames and read in
    kwargs['sep'] = sep
    kwargs['header'] = header
    data = [pd.read_table(_, **kwargs) for _ in fnames]

    # Concatenate
    data = data[0] if len(data) == 1 else pd.concat(data)

    # If verbose, note the shape of the data and the runtime
    if verbose:
        # noinspection PyUnboundLocalVariable
        end_time = time.time()
        # noinspection PyUnboundLocalVariable
        print(f'file loaded with shape {data.shape} in {int(end_time - start_time)} seconds')

    # If header is None and index_col is defined, reset columns
    if header is None and kwargs.get('index_col', None) is not None:
        data.columns = np.arange(len(data.columns))

    # Return
    return data
