from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.http import Http404
from django.shortcuts import render

from random import Random
from markdown2 import Markdown
from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def search(request):
    entries = util.list_entries()
    title = request.GET["search"]
    if title:
        if title in entries:
            return HttpResponseRedirect(reverse("encyclopedia:entry", kwargs={'title': title}))
        else:
            matches = [entry for entry in entries if title in entry.lower() ]
            return render(request, "encyclopedia/search.html", {
                "search": title,
                "matches": matches
            })
    return HttpResponseRedirect(reverse("encyclopedia:index"))
                

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

def random(request):
    title = Random().choice(util.list_entries())
    return HttpResponseRedirect(reverse("encyclopedia:entry", kwargs={'title': title}))

