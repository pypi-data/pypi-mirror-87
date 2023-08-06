import pandas as pd


def absolute_diff(row):
    """
    Compute the absolute difference given a list of length 2
    :param row: a list with length of 2 [row_0, row_1]
    :return |row_0 - row_1|
    """
    return abs(row[0] - row[1])


def diff(dataframe_a, dataframe_b, func):
    """
    Given dataframe_a and dataframe_b, compute a difference between each row-wise element of both dataframes.
    Missing values are discarded (drop nans) and operations only applicable to numeric values
    :param dataframe_a: first dataframe
    :param dataframe_b: second dataframe
    :param func: a difference function (see row_diff.absolute_diff)
    """
    # make this more generic (i.e. outer)
    if dataframe_a.index.name != dataframe_b.index.name:
        raise ValueError('a common index name is required in both frames, please see dataframe_a.index.name')
    df = pd.merge(dataframe_a, dataframe_b, how='inner', on=dataframe_a.index.name, suffixes=('_a', '_b'))
    columns = dataframe_a.columns

    rlist = []
    for col in columns:
        print(col)
        s = df[['{}_a'.format(col), '{}_b'.format(col)]].dropna().apply(func, axis=1)
        rlist.append({'label': col,
                      'ave(f)': sum(s) / len(s),
                      'min(f)': s.min(),
                      'max(f)': s.max()})
    return rlist
