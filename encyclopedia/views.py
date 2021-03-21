from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib import messages

from . import util
from . import forms


def index(request):
    if request.method == "GET":
        if len(request.GET) != 0:
            search = request.GET["q"]
            return render(request, "encyclopedia/index.html", {"entries": util.searchEntry(search)})
    return render(request, "encyclopedia/index.html",
                  {"entries": util.list_entries()})


def wikis(request, title):
    return render(request, "encyclopedia/wiki.html", {
        "title": title.capitalize(),
        "wikiInfo": util.get_entry(title)
    })


def newPage(request):
    nPageForm = forms.NewPageForm()
    if request.method == "POST":
        form = forms.NewPageForm(request.POST)
        if form.is_valid():
            fTitle = form.cleaned_data["title"]
            fText = form.cleaned_data["text"]
            if util.get_entry(fTitle) == None:
                util.save_entry(fTitle, fText)
                return HttpResponseRedirect(reverse("encyclopedia:index"))
            else:
                messages.add_message(request, messages.INFO,
                                     f"ERROR: the wiki {fTitle} already exist")
                return render(request, "encyclopedia/newPage.html", {"form": form})
        else:
            return render(request, "encyclopedia/newPage.html", {"form": form})
    return render(request, "encyclopedia/newPage.html", {"form": nPageForm})
