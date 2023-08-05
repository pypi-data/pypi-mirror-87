"""
Visualizing Numbers Appropriately
"""

from IPython.display import HTML
from spacy.pipeline import EntityRuler
from spacy import displacy
from spacy.matcher import Matcher
import re
import spacy
import warnings

# def summarize_size(num):
#     return f"{round(len(x)/1000.0)}k"


def summarize_size(l):
    return comma_seperate(len(l))

def comma_seperate(num:int): 
    return f"{num:,}"

def summarize(num, suffix='', prefix='~ ', base=1000.0, value_type="currency"):
    """
    # based on https://stackoverflow.com/questions/1094841/reusable-library-to-get-human-readable-version-of-file-size
    # https://pypi.org/project/humanize/
    # https://www.thoughtco.com/zeros-in-million-billion-trillion-2312346
    """
    units = {
        "currency": ['', ' Thousand', ' Million', ' Billion', ' Trillion', ' Quadrillion', ' Quintillion'],
        "memory": ['', 'Ki', 'Mi', 'Gi', 'Ti', 'Pi', 'Ei', 'Zi'],
    }.get(value_type, [''])

    for unit in units:
        if abs(num) < base:
            if isinstance(num, int): 
                summary = f"{prefix}{num}{unit}{suffix}"
            else:
                summary = f"{prefix}{num:3.1f}{unit}{suffix}"
            return summary
        num /= base
    
    # Number too big ...
    summary = f"{num:3.1f}{unit}{suffix}"
    recursive_summary = summarize(
        num, suffix=suffix, prefix='', base=base, value_type=value_type
    )
    return f"{prefix}{recursive_summary} * 1{units[-1]}"


def construct_task_nlp(unit:str):
    nlp = spacy.blank("en")
    ruler = EntityRuler(nlp)
    patterns = [
        {
            "label": unit,
            "pattern": [
                {"TEXT": {"REGEX": "[0-9,]+"}}
            ]
        }
    ]
    ruler.add_patterns(patterns)
    nlp.add_pipe(ruler)
    return nlp


def display_number(n:int, unit:str="NUMBER", big=True, color_choice="dark-blue"):
    """
    # https://www.eggradients.com/
    """
    if not unit.upper() == unit:
        warnings.warn("kwarg <unit> must be in all caps.")
        return n

    colors = {
        "purple": "linear-gradient(90deg, #aa9cfc, #fc9ce7)",
        "dark-blue": "linear-gradient(315deg,  #2a2a72 0%, #009ffd 74%)"
    }
    colors = {
        unit: colors[color_choice],
    }
    options = {
        "ents": [
            unit,
        ],
        "colors": colors
    }
    nlp = construct_task_nlp(unit)
    doc = nlp(str(n))
    html = HTML(displacy.render(
        doc,
        page=True, minify=False, jupyter=False, style="ent", options=options
    ))
    if big:
        return make_tag_bigger(html)
    return html


def make_tag_bigger(html, color="white"):
    return HTML(html.data.replace("line-height: 2.5", "line-height: 1.0").replace(
        "padding: 0.45em 0.6em; margin: 0 0.25em; line-height: 1; border-radius: 0.35em;",
        f"padding: 0.30em 0.6em; margin: 0 0.50em; line-height: 2; border-radius: 0.35em; font-size: 3em; color: {color}"
    ))
