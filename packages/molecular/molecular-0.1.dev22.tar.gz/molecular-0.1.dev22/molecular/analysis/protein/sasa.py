import yaml
import os
import pandas as pd

include_dir = os.path.abspath(__file__ + '../../../../_include')


# Read relative SASA
def get_relative_sasa(sequence=None):
    """
    Get relative SASA for sequence.

    Parameters
    ----------
    sequence : np.ndarray

    Returns
    -------

    """

    # Read in relative SASA
    with open(os.path.join(include_dir, 'protein', 'relative_sasa.yml'), 'r') as stream:
        data = yaml.safe_load(stream.read())

    # Convert to Series
    relative_sasa = pd.Series(data).rename('relative_sasa')

    # Result
    result = relative_sasa
    if sequence is not None:
        result = relative_sasa.loc[sequence]

    # Return
    return result


class SurfaceArea:
    pass


if __name__ == '__main__':
    print(get_relative_sasa())
