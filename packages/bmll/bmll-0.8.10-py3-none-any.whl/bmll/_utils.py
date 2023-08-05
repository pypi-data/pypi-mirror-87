import pandas as pd


__all__ = ('to_pandas', 'paginate', 'to_list_of_str')


ID_COL_TYPE = 'Int64' if pd.__version__ >= '0.24.0' else 'object'


def to_pandas(table):
    """Return a pandas DataFrame from a Table response."""
    df = pd.DataFrame(data=table['data'], columns=table['columns'])

    if 'Date' in df.columns:
        df['Date'] = pd.to_datetime(df['Date'])

    if 'ObjectId' in df.columns:
        df['ObjectId'] = df['ObjectId'].astype(ID_COL_TYPE)

    return df


def paginate(request):
    table = request()
    token = table.get('token')

    while token:
        page = request(token=token)
        if isinstance(table['data'], dict):
            table['data'].update(page['data'])
        else:
            table['data'].extend(page['data'])
        token = page.get('token')

    return table


def to_list_of_str(x):
    """Converts variable to list. int -> list, str -> list, list -> list."""
    if hasattr(x, '__iter__') and not isinstance(x, str):
        return [str(y) for y in x]
    return [str(x)]
