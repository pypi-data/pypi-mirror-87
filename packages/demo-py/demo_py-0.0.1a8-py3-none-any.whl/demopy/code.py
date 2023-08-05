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
