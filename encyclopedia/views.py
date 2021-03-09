from django.shortcuts import render

from . import util


def index(request):
    return render(request, "encyclopedia/index.html",
                  {"entries": util.list_entries()})


def wikis(request, title):
    return render(request, "encyclopedia/wiki.html", {
        "title": title.capitalize(),
        "wikiInfo": util.get_entry(title)
    })