import yaml
import os
import pandas as pd

include_dir = os.path.abspath(__file__ + '../../../../_include')


# Read relative SASA
def get_relative_sasa():
    """
    Relative SASA

    Returns
    -------

    """

    with open(os.path.join(include_dir, 'protein', 'relative_sasa.yml'), 'r') as stream:
        relative_sasa = yaml.safe_load(stream.read())
    return pd.Series(relative_sasa).rename('relative_sasa')


class SurfaceArea:
    pass


if __name__ == '__main__':
    print(get_relative_sasa())
