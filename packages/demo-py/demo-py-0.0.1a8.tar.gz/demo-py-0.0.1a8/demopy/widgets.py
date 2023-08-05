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

def button(text):
    return widgets.Checkbox(
        value=False,
        description=text,
        disabled=False
    )


def container(stuff):
    return widgets.VBox(stuff)


def to_output(content, display_function=display):
    """
    returns how ipython displays content by default
    """
    x = widgets.Output()
    with x:
        display_function(content)
    return x

def tab_with_content(content_dict, key_order=lambda l: l):
    """
    Creates a tab with dicts where keys are tabnames and content are the content of the tab ...
    """
    tab = widgets.Tab()
    keys = key_order(list(content_dict.keys()))
    tab.children = [content_dict[k] for k in keys]
    for (i,title) in enumerate(keys):
        tab.set_title(i, title)
    return tab


def tab_with_side_by_side_content(content_dict, key_order=lambda l: l):
    """
    """
    return tab_with_content(
        {
            k: widgets.HBox(v)
            for k, v in content_dict.items()
        },
        key_order=key_order
    )

def set_id_for_dom_element_of_output_for_current_cell(_id):
    display(Javascript('console.log(element.get(0)); element.get(0).id = "{}";'.format(_id)))


def json_code(j):
    return Code(data=json.dumps(j, indent=4), language="json")


class InteractiveJSON(object):
    def __init__(self, json_data):
        if isinstance(json_data, dict):
            self.json_str = json.dumps(json_data)
        elif isinstance(json_data, JSON):
            self.json_str = json_data.data
        else:
            self.json_str = json_data
        self.uuid = str(uuid.uuid4())

    def _ipython_display_(self):
        display_html('<div id="{}" style="height: 600px; width:100%;"></div>'.format(self.uuid),
            raw=True
        )
        display_javascript("""
        require(["https://rawgit.com/caldwell/renderjson/master/renderjson.js"], function() {
          renderjson.set_icons('+', '-');
          renderjson.set_show_to_level("2");
          document.getElementById('%s').appendChild(renderjson(%s))
        });
        """ % (self.uuid, self.json_str), raw=True)



def string_to_md_list(s):
    return Markdown("\n".join([
        f"* {x}"
        for x in s.split('.')
        if x
    ]))
