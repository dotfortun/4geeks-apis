from pathlib import Path
import os
import re

from django.http import HttpResponse, HttpRequest
from django.template.loader import get_template

import markdown
import nh3


def home_page(request: HttpRequest):
    html = get_template("base.html")
    return HttpResponse(html.render(
        request=request,
        context={
            "page_title": "4Geeks Api Playground",
        }
    ))


def get_pages(request: HttpRequest, dir_path=""):
    html = get_template("base.html")
    md_file = None
    lang = request.headers.get('Accept-Language', 'en-US').split(",")[0]

    # This can definitely be rewritten.
    if lang == "es-ES":
        if os.path.isfile(md_path := ("./pages/" + dir_path)):
            f_path = md_path
        elif os.path.isfile(md_path := ("./pages/" + dir_path + '.es.md')):
            f_path = md_path
        elif os.path.isfile(
            md_path := ("./pages/" + re.sub(r'\.\w+', '.es.md', dir_path.lower()))
        ):
            f_path = md_path
        else:
            f_path = "./pages/" + dir_path + "/index.es.md"
    else:
        if os.path.isfile(md_path := ("./pages/" + dir_path)):
            f_path = md_path
        elif os.path.isfile(md_path := ("./pages/" + dir_path + '.md')):
            f_path = md_path
        elif os.path.isfile(
            md_path := ("./pages/" + re.sub(r'\.\w+', '.md', dir_path.lower()))
        ):
            f_path = md_path
        else:
            f_path = "./pages/" + dir_path + "/index.md"

    with open(f_path, "rt") as base:
        md_file = base.read()

    md = markdown.Markdown(
        extensions=["meta", "fenced_code"]
    )

    md_html = nh3.clean(
        md.convert(md_file or ""),
        attributes={
            **nh3.ALLOWED_ATTRIBUTES,
            'a': {*nh3.ALLOWED_ATTRIBUTES['a'], 'target'}
        }
    )

    return HttpResponse(html.render(
        request=request,
        context={
            "page_title": " ".join(md.Meta.get("title", ["But why?"])),
            "content": md_html,
            "debug": {
                "dir_path": dir_path,
            }
        }
    ))
