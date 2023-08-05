import pandas as pd
import ipywidgets as widgets
from IPython.display import display, Markdown, Latex, TextDisplayObject, TextDisplayObject

# https://ipywidgets.readthedocs.io/en/latest/examples/Widget%20List.html
# https://ipywidgets.readthedocs.io/en/latest/examples/Output%20Widget.html
# https://stackoverflow.com/questions/36288670/how-to-programmatically-generate-markdown-output-in-jupyter-notebooks
# https://ipywidgets.readthedocs.io/en/latest/examples/Layout%20Templates.html


def output(content, layout={'border': '1px solid black'}):
    """
    returns how ipython displays content by default
    """
    x = widgets.Output(layout=layout)
    with x:
        display(content)
    return x


def fix(lines):
    return "\n".join([x for x in lines if x.strip()])


def markdownify_sql(text):
    sql = "\n".join([
        f"{ll}  "
        for l in text.split("\n")
        for ll in [l.replace("\t", "    ")]
    ])
    return Markdown(f"```sql\n{sql}\n```")


def accordian(*args, titles=[], **kwargs):
    x = widgets.Accordion(args, **kwargs)
    for i, t in enumerate(titles):
        x.set_title(i, t)
    # Fold / Collapse accordian
    x.selected_index = None
    return x


def run_query(filename=None, connection=None, query=None, query_params_args=[], query_params_kwargs={}):
    # Get Query
    if query is None:
        with open(filename) as fh:
            sql_content = fh.read()
    else:
        sql_content = query
    # Apply Query Parameters
    if query_params_args:
        sql_content = sql_content.format(*query_params_args)
    if query_params_kwargs:
        sql_content = sql_content.format(**query_params_kwargs)
    # Remove comments
    QUERY = fix([
        x
        for x in sql_content.split("\n")
        if not x.strip().startswith("--")
    ])
    # Run Query
    df = pd.read_sql_query(QUERY, con=connection)
    # Format Results
    items = [
        #         output(Markdown('## Query')),
        accordian(output(markdownify_sql(QUERY)), titles=["Query"]),
        widgets.VBox([
            output(Markdown('## Results')),
            output(df.head()),
            output(Markdown('## Result Size')),
            output(Markdown(str(df.shape)))
        ])
    ]
    # gridbox = widgets.GridBox(items, layout=widgets.Layout(grid_template_columns="repeat(2, 50%)"))
    gridbox = widgets.GridBox(items, layout=widgets.Layout(
        grid_template_columns="75% 25%"))
    return (df, gridbox)
