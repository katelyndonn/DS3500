""" reusable functions for future use """


def num_filter(df, col, range):
    """ takes a dataframe and filters a column by a min and max range
        given as a list pair (ex: [10, 20]) """
    filtered_df = df[(df[col] >= range[0]) & (df[col] <= range[1])]
    return filtered_df


def sort_limit_dict(input_dict, desc=True, limit=None):
    """ takes a dictionary with int/float values, sorts it by values,
        and returns a limited amount of results in a new dictionary """
    sorted_dict = {k: v for k, v in sorted(input_dict.items(),
                                           key=lambda item: item[1], reverse=desc)}

    if limit is not None:
        return dict(itertools.islice(sorted_dict.items(), limit))
    else:
        return sorted_dict
