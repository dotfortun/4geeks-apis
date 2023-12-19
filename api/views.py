from pathlib import PurePath
import re

from django.http import HttpResponse, HttpRequest
from django.template.loader import get_template

import markdown
from html_sanitizer import Sanitizer


def get_pages(request: HttpRequest, dir_path=""):
    html = get_template("base.html")
    f = None
    path = PurePath(dir_path)

    md_file = "index.md"
    f_path = "/".join([*path.parts, md_file])
    if re.search(r'\.htm', dir_path.lower()):
        md_file = "/" + path.stem + ".md"
        f_path = "/".join([*path.parts[:-1], md_file])

    with open("./pages/" + f_path, "rt") as base:
        f = base.read()

    md = markdown.Markdown(
        extensions=["meta", "fenced_code"]
    )

    sanitzer = Sanitizer()
    md_html = sanitzer.sanitize(
        md.convert(f or "")
    )

    page_title = " ".join(md.Meta.get("title", ["But why?"]))

    return HttpResponse(html.render(
        request=request,
        context={
            "page_title": page_title,
            "content": md_html,
            "debug": {
                "md_path": "./pages/" + "/".join(path.parts[:-1]) + md_file,
                "dir_path": dir_path,
                "pure_path": path.parts,
            },
        }
    ))
