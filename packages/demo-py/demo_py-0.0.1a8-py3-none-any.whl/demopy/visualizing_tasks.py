import spacy
import re
from spacy.matcher import Matcher
from spacy import displacy
from spacy.pipeline import EntityRuler
from IPython.display import HTML

# https://spacy.io/api/top-level#spacy.blank
# https://spacy.io/usage/rule-based-matching#entityruler-usag
# https://spacy.io/usage/visualizers
# https://spacy.io/usage/visualizers#ent


def date_regex(prefix): 
    return {"TEXT": {"REGEX": f"{prefix}[0-9]{{4}}"}}


def construct_task_nlp():
    nlp = spacy.blank("en")
    ruler = EntityRuler(nlp)
    patterns = [
        {
            "label": "DONE",
            "pattern": [{"ORTH": "-"}, {"ORTH": "["}, {"TEXT": {"REGEX": "[xX]"}}, {"ORTH": "]"}]
        },
        {
            "label": "BACKLOG",
            "pattern": [{"ORTH": "-"}, {"ORTH": "["}, {"ORTH": ">"}, {"ORTH": "]"}]
        },
        {
            "label": "TODO",
            "pattern": [{"ORTH": "-"}, {"ORTH": "["}, {"ORTH": "]"}]
        },
        {
            "label": "DOING",
            "pattern": [{"ORTH": "-"}, {"ORTH": "["}, {"ORTH": "."}, {"ORTH": "]"}]
        },
        # Add an overdue?
        {
            "label": "COMPLETED-ON",
            "pattern": [
                date_regex("@done[(]"),
                {"ORTH": "-"},
                # Month
                {"TEXT": {"REGEX": "[0-9]{2}"}},
                {"ORTH": "-"},
                # Day
                {"TEXT": {"REGEX": "[0-9]{2}"}},
                # Space get eaten
                # Time
                {"TEXT": {"REGEX": "[0-9]{2}:[0-9]{2}"}},
                {"TEXT": {"REGEX": "[aApP][mM]"}},
                {"ORTH": ")"}
            ]
        },
        {
            "label": "STARTED-ON",
            "pattern": [
                date_regex("[|]"),
                {"ORTH": "-"},
                # Month
                {"TEXT": {"REGEX": "[0-9]{2}"}},
                {"ORTH": "-"},
                # Day
                {"TEXT": {"REGEX": "[0-9]{2}"}}
            ]
        },
        {
            "label": "POSTPONED-TIL",
            "pattern": [
                {"ORTH": ">"},
                date_regex(""),
                {"ORTH": "-"},
                # Month
                {"TEXT": {"REGEX": "[0-9]{2}"}},
                {"ORTH": "-"},
                # Day
                {"TEXT": {"REGEX": "[0-9]{2}"}}

            ]
        },
        {
            "label": "SCHEDULED-FOR",
            "pattern": [
                date_regex("@"),
                {"ORTH": "-"},
                # Month
                {"TEXT": {"REGEX": "[0-9]{2}"}},
                {"ORTH": "-"},
                # Day
                {"TEXT": {"REGEX": "[0-9]{2}"}}

            ]
        },
        {
            "label": "HASHTAG",
            "pattern": [{"ORTH": "#"}, {"TEXT": {"REGEX": "[a-zA-Z0-9-_/>]+"}}]
        }
    ]
    ruler.add_patterns(patterns)
    nlp.add_pipe(ruler)
    return nlp


def display_tasks(list_of_tasks):
    """
    # https://www.eggradients.com/
    """
    colors = {
        "BACKLOG": "linear-gradient(90deg, #aa9cfc, #fc9ce7)",
        "POSTPONED-TIL": "linear-gradient(90deg, #aa9cfc, #fc9ce7)",
        "TODO": "linear-gradient(90deg, #83EAF1, #63A4FF)",
        "SCHEDULED-FOR": "linear-gradient(90deg, #83EAF1, #63A4FF)",
        "DOING": "linear-gradient(90deg, #80FF72, #7EE8FA)",
        "STARTED-ON": "linear-gradient(90deg, #80FF72, #7EE8FA)",
        "DONE": "linear-gradient(90deg, #FFD8CB, #F9D29D)",
        "COMPLETED-ON": "linear-gradient(90deg, #FFD8CB, #F9D29D)",
        "HASHTAG": "linear-gradient(90deg, #F5E3E6, #D9E4F5)"
    }
    options = {
        "ents": [
            "BACKLOG",
            "TODO",
            "DOING",
            "DONE",
            "POSTPONED-TIL",
            "SCHEDULED-FOR",
            "STARTED-ON",
            "COMPLETED-ON",
            "HASHTAG"
        ],
        "colors": colors
    }
    nlp = construct_task_nlp()
    doc = nlp("\n".join(list_of_tasks))
    return HTML(displacy.render(
        doc, 
        page=True, minify=False, jupyter=False, style="ent", options=options,
        font="Roboto"
    ))
    # if return_html:
    # return displacy.render(doc, jupyter=True, style="ent", options=options)
