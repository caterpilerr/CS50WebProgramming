from django.contrib import messages
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
    query = request.GET["search"]
    if query:
        if query in entries:
            return HttpResponseRedirect(reverse("encyclopedia:entry", kwargs={'title': query}))
        else:
            matches = [entry for entry in entries if query.lower() in entry.lower()]
            return render(request, "encyclopedia/search.html", {
                "search": query,
                "matches": matches
            })
    return HttpResponseRedirect(reverse("encyclopedia:index"))
                

def entry(request, title):
    content = util.get_entry(title)
    if not content:
        content = f"#{title}\n Wiki doesn't have article with this exact name."
    else:    
        md_converter = Markdown()
        content = md_converter.convert(content)
    return render(request, "encyclopedia/entry.html", {
        "title": title,
        "content": content
    })

def random(request):
    title = Random().choice(util.list_entries())
    return HttpResponseRedirect(reverse("encyclopedia:entry", kwargs={'title': title}))


def new_entry(request):
    if request.method == 'POST':
        title = request.POST["title"]
        content = request.POST["page_content"].encode()
        if title:
            entries = util.list_entries()
            if not title in entries:
                util.save_entry(title, content)
            else:
                messages.error(request, 'Page with same title already exists!')
    return render(request, "encyclopedia/new_entry.html")

