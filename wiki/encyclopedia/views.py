from django.http import Http404
from django.shortcuts import render

from markdown2 import Markdown
from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    content = util.get_entry(title)
    if not content:
        raise Http404
    md_converter = Markdown()
    content = md_converter.convert(content)
    return render(request, 'encyclopedia/entry.html', {
        "title": title,
        "content": content
    })


