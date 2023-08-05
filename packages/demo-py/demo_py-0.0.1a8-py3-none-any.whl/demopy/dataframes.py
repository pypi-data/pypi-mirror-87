import numpy as np
from IPython.display import display, Markdown


# https://stackoverflow.com/questions/17530542/how-to-add-pandas-data-to-an-existing-csv-file
def append_df_to_file(df, filename, **kwargs):
    with open(filename, 'a') as f:
        df.to_csv(f, header=f.tell() == 0, **kwargs)


highlight_css = {
    "background-color": "yellow",
    "opacity": "0.75"
}


def construct_column_highlighting_function(column_name, css):
    '''
    highlight the maximum in a Series yellow.
    '''
    css = "; ".join([f"{k}: {v}" for k, v in css.items()])

    def inner(column_of_data):
        return [
            css if column_of_data.name == column_name else ''
            for x in np.arange(len(column_of_data))
        ]
    return inner


def highlight_columns(df, *columns, css=highlight_css):
    # https://pandas.pydata.org/pandas-docs/stable/user_guide/style.html#Building-Styles-Summary
    # Column wise ...
    if len(columns) < 1:
        return df.style

    return highlight_columns(df, *columns[:-1], css=css).apply(
        construct_column_highlighting_function(columns[-1], css),
        axis=0
    )


def summarize_df(df, head=2, header=None):
    if header:
        display(Markdown(f"# {header}"))
    # Transition.discovery_pad().data_dictionary(df_posts, stylise=True)
    display(df.shape)
    display(df.head(head))
    display(Markdown("---"))


def split_df(df, criteria):
    a = df[criteria(df)]
    b = df[~criteria(df)]
    return a, b
