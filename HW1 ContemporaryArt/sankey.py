
"""
sankey.py: A reusable library for sankey visualizations
"""

import plotly.graph_objects as go
import pandas as pd


def _code_mapping(df, src, targ):
    # Get distinct labels
    labels = sorted(list(set(list(df[src]) + list(df[targ]))))

    # Get integer codes
    codes = list(range(len(labels)))

    # Create label to code mapping
    lc_map = dict(zip(labels, codes))

    # Substitute names for codes in dataframe
    df = df.replace({src: lc_map, targ: lc_map})

    return df, labels


def make_sankey(df, *cols, vals=None, **kwargs):
    """ Create a sankey diagram linking src values to
    target values with thickness vals """

    if len(cols) > 2:
        # if the cols length is greater than 2, stack columns
        df = stack_columns(df, *cols)
        src, targ = 'src', 'targ'
    else:
        src = cols[0]
        targ = cols[1]

    if vals:
        values = df[vals]
    else:
        values = [1] * len(df)

    # Step 2
    # grouping data by src and tg
    # and counting artists
    df = df.groupby([src, targ]).size().reset_index(name='Count')

    # Step 3
    # filter out rows where decade is 0
    # turn the ints into strings
    df = df[df[targ] != 0]
    df[targ] = df[targ].astype(str)

    # Step 4
    # filter out rows where artist count is below threshold
    df = df[df.Count >= 20]

    # map out the code accordingly
    df, labels = _code_mapping(df, src, targ)
    link = {'source': df[src], 'target': df[targ], 'value': values}
    pad = kwargs.get('pad', 50)

    node = {'label': labels, 'pad': pad}
    sk = go.Sankey(link=link, node=node)
    fig = go.Figure(sk)
    fig.show()


def stack_columns(df, *cols):
    """
    :param df: dataframe
    :param cols: the source, target, and whatever other columns inputted
    :param vals: width
    :return: stacked df
    """
    list1 = [cols[0], cols[1]]
    list2 = [cols[1], cols[2]]

    # make the pairs of data
    pair1 = df[list1]
    pair1.columns = ['src', 'targ']
    pair2 = df[list2]
    pair2.columns = ['src', 'targ']

    # stack the data
    stacked = pd.concat([pair1, pair2], axis=0)

    return stacked
