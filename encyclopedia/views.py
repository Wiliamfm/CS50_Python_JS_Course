import re
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib import messages
import random
import markdown

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
    print((markdown.markdown('<div markdown="1">' +
                             util.get_entry(title)+'</div>', extensions=["md_in_html"])))
    return render(request, "encyclopedia/wiki.html", {
        "title": title.capitalize(),
        "wikiInfo": markdown.markdown(util.get_entry(title), extensions=['fenced_code'])
        # "wikiInfo": util.get_entry(title)
    })


def editPage(request, title):
    form = forms.EditPageForm(initial={"text": util.get_entry(title)})
    if request.method == "POST":
        f = forms.EditPageForm(request.POST)
        if f.is_valid():
            util.save_entry(title, f.cleaned_data["text"])
        return HttpResponseRedirect(reverse("encyclopedia:index"))
    return render(request, "encyclopedia/editPage.html", {"title": title, "form": form})


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


def randomWiki(request):
    return wikis(request, random.choice(util.list_entries()))
