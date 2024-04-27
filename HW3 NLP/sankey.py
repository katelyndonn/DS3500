"""
sankey.py: a reusable library for sankey visualizations
"""

import plotly.graph_objects as go
import pandas as pd


def _code_mapping(df, src, targ):

    # Get distinct labels
    labels = set((df[src].to_list() + df[targ].to_list()))
    labels = sorted([i for i in labels])

    # Get integer codes
    codes = (range(len(labels)))

    # Create label to code mapping
    lc_map = dict(zip(labels, codes))

    # Substitute names for codes in dataframe
    df = df.replace({src: lc_map, targ: lc_map})

    # return df, labels
    return df, labels


def _stack_columns(df, cols, vals=None):
    """ stack columns and return a concat dataframe """
    stack_list = []

    for i in range(len(cols) - 1):
        ndf = df[[cols[i], cols[i + 1], vals]]
        ndf.columns = ['src', 'targ', 'vals']
        stack_list.append(ndf)

    stacked = pd.concat(stack_list, axis=0)

    return stacked


def make_sankey(df, *cols, vals=None, **kwargs):
    """ Create a sankey diagram linking src values to target
    values with thickness vals from a list of columns"""
    if vals is None:
        vals = 'vals'

    if len(cols) > 2:
        df = _stack_columns(df, cols, vals=vals)
        src, targ, vals = 'src', 'targ', 'vals'
    else:
        src = cols[0]
        targ = cols[1]

    df, labels = _code_mapping(df, src, targ)
    link = {'source': df[src], 'target': df[targ], 'value': df[vals]}
    pad = kwargs.get('pad', 50)

    node = {'label': labels, 'pad': pad}
    sk = go.Sankey(link=link, node=node)
    fig = go.Figure(sk)
    fig.show()



