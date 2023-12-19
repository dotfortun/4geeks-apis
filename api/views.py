from django.http import HttpResponse, HttpRequest
from django.template.loader import get_template

import markdown


def index(request: HttpRequest, dir_path=""):
    html = get_template("base.html")
    f = None
    with open("./pages/" + dir_path + "/index.md", "rt") as base:
        f = base.read()

    md = markdown.Markdown(
        extensions=["meta", "fenced_code"]
    )

    return HttpResponse(html.render(
        request=request,
        context={
            "page_title": md.Meta.get("title", ""),
            "content": md.convert(f or "")
        }
    ))
