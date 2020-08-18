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
    if request.method == "POST":
        title = request.POST["title"]
        content = request.POST["content"]
        if title:
            entries = util.list_entries()
            if not title.lower() in (entry.lower() for entry in entries):
                util.save_entry(title, content.encode("utf-8"))
                messages.success(request, "New entry has been successfully saved!")
                return HttpResponseRedirect(reverse("encyclopedia:entry", kwargs={'title': title}))
            else:
                messages.error(request, "Page with same title already exists!")
        elif content:
            messages.warning(request, "You are trying to save entry with no title!")
    return render(request, "encyclopedia/new_entry.html")


def edit_entry(request):
    if request.method == "GET":
        title = request.GET["title"]
        content = util.get_entry(title)
        return render(request, "encyclopedia/edit_entry.html", {
            "title" : title,
            "content" : content
            })
    else:
        title = request.POST["title"]
        content = request.POST["content"]
        if content == util.get_entry(title):
            messages.warning(request, "No differences have been made!")
            return render(request, "encyclopedia/edit_entry.html", {
                "title" : title,
                "content" : content
            })
        else:
            util.save_entry(title, content.encode("utf-8"))
            messages.success(request, "Entry have been successfully modified!")
            return HttpResponseRedirect(reverse("encyclopedia:entry", kwargs={'title': title}))
        

