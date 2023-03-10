from django.shortcuts import render
from django.http import HttpResponse
from django import forms
from random import randint


import markdown2

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request,title):
    if util.get_entry(title) == None:
        return render(request, "encyclopedia/apology.html", {
            "title": title
        })
    else:
        return render(request, "encyclopedia/entrypage.html", {
            "entry": markdown2.markdown(util.get_entry(title)),
            "entryTitle" : title
    })

def search(request):
    input = request.GET.get("q")
    entries = util.list_entries()

    pages = []
    for entry in entries:
        if input.upper() == entry.upper():
            return render (request, "encyclopedia/entrypage.html", {
                "entry": markdown2.markdown(util.get_entry(entry)),
                "entryTitle" : entry
            })
        elif input.upper() in entry.upper():
            pages.append(entry)
    if len(pages) == 0:
        return render(request, "encyclopedia/apology.html", {
            "title" : input
        })
    else:
        return render (request, "encyclopedia/search.html", {
            "entries": pages
        })

class NewPageForm(forms.Form):
    title = forms.CharField(label="Title", widget=forms.TextInput(attrs={'placeholder': 'Title'}))
    content = forms.CharField(label="Content", widget=forms.Textarea(attrs={'placeholder': 'Content'}))

def newpage(request):
    if request.method == "POST":
        form = NewPageForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            entries = util.list_entries()
            for entry in entries:
                if entry == title:
                        return render(request, "encyclopedia/PageExist.html",{
                        "title": title
                        })
            util.save_entry(title, content)
            return render (request, "encyclopedia/entrypage.html", {
                "entry": markdown2.markdown(util.get_entry(title)),
                "entryTitle" : title
            })
        else:
            return render(request, "encyclopeida/newpage.html", {
                "form": form
            })
    else:
        return render (request, "encyclopedia/newpage.html",{
            "form":NewPageForm
        })

def editpage(request):
    title = request.POST.get('entry')
    content = util.get_entry(title)
    return render(request, "encyclopedia/editpage.html", {
        "title" : title,
        "content" : content
    })

def saveEdit(request):
    title = request.POST.get("title")
    content = request.POST.get("content")
    util.save_entry(title, content)
    return render (request, "encyclopedia/entrypage.html", {
        "entry": markdown2.markdown(util.get_entry(title)),
        "entryTitle" : title
    })

def random(request):
    entries = util.list_entries()
    listlen = len(entries)
    title = entries[randint(0,listlen-1)]
    return render (request, "encyclopedia/entrypage.html", {
        "entry": markdown2.markdown(util.get_entry(title)),
        "entryTitle" : title
    })






