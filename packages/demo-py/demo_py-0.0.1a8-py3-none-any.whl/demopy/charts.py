import textwrap
import collections
import io
import itertools
import json
import uuid
from typing import Any, AnyStr, Mapping, NamedTuple, Optional

import ipywidgets as widgets
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from IPython.core.display import HTML, display
from IPython.display import (JSON, SVG, Image, Javascript, Markdown, Pretty,
                             display_html, display_javascript)
from IPython.display import JSON, display_json, Code

# https://www.datacamp.com/community/tutorials/wordcloud-python


def extract_figure_as_image(w, h) -> widgets.Image :
    image = io.BytesIO()
    plt.savefig(image, format="png")
    image.seek(0)
    img = widgets.Image(
        value=image.read(),
        format='png',
        width=w,
        height=h
    )
    img.layout.margin = "0 0 0 0"
    return img


def bar_chart(values: dict, title="Chart", yaxis="y", xaxis="x", width_factor=35, height_factor=15, str_width=5):
    # print(values)
    # https://stackoverflow.com/questions/8598673/how-to-save-a-pylab-figure-into-in-memory-file-which-can-be-read-into-pil-image
    fig = plt.figure(figsize=(width_factor, height_factor))
    # TODO - instead of using textwrap, tilt them
    x = ["\n".join(textwrap.wrap(i, width=5)) for i in list(values.keys())]
    bar_num = np.arange(len(x))
    y = list(values.values())
    plt.bar(bar_num, y, alpha=0.5, align='center', width=0.5)
    plt.xticks(bar_num, x)
    # plt.ylabel(yaxis)
    # plt.xlabel(xaxis)
    # plt.title(title)
    # plt.show(fig)
    img = extract_figure_as_image(100*width_factor, 100*height_factor)
    plt.close(fig)
    return img


def plot_pie(d):
    # Pie chart, where the slices will be ordered and plotted counter-clockwise:
    keys = [x for x in d.keys()]
    values = [x for x in d.values()]
    labels = [f"{d[k]*100:2.1f}%: {k}" for k in keys]
    # labels = [f"{d[k]['value']*100:2.1f}%: {k}" for k in keys]
    sizes = np.asarray(values, np.float32)
    # sizes = [v["value"] for v in values]
    if sizes.sum() >= 1.0:
        # sizes = np.asarray([x - (16.0 * e) for x in sizes], np.float32)
        sizes = sizes - np.finfo(np.float32).eps
    # print(sizes, sum(sizes), sizes.sum(), labels)
    fig1, ax1 = plt.subplots(figsize=(12.5, 7.5))
    ax1.pie(sizes, labels=None, shadow=True, startangle=90, normalize=False)
    # ax1.pie(sizes, labels=None, autopct='%1.1f%%', shadow=True, startangle=90)
    # ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.legend(labels, loc="lower right", prop={'size': 10})
    image = extract_figure_as_image(1250, 750)
    plt.tight_layout()
    plt.close(fig1)
    return image


def plot_columns_of_counts(df, columns, styles, mask=lambda x: x, identifier="day"):
    # Plotting
    fig, _ = plt.subplots()
    df = df[[identifier]+columns]
    df_agg = df.groupby([identifier], as_index=False)[columns].sum()
    df_agg = df_agg.set_index(identifier)
    for i, c in enumerate(columns):
        df_agg[mask(df_agg)][c].plot(**styles[i])
    plt.legend(loc='lower center', shadow=True)
    img = extract_figure_as_image(1000, 500)
    plt.close(fig)
    return img
    # plt.savefig('baseline_pred_comparision.pdf', bbox_inches='tight')
