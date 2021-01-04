from django.shortcuts import render, redirect
from . import util

from markdown2 import Markdown
import re # regular expression
import random as rdm

def index(request):
    """
    List view of wiki entries
    """
    return render(request, "encyclopedia/index.html", { #This view returns a template from /templates folder
        "entries": util.list_entries()
    })


def search(request):
    """
    Search wiki entries
    """
    search_query = request.POST.get('q')
    entries = util.list_entries()

    #check if search_query matches entry titles?
    if(search_query in entries):
        return redirect('/wiki/'+search_query)
    else:
        #return a list of alike entries
        results = []

        for e in entries:
            r = re.search(search_query, e, re.IGNORECASE)
            if(r is not None):
                results.append(e)

        context = {
            "search_query": search_query,
            "entries": results  #a refined list
        }
        return render(request, "encyclopedia/search.html", context)


def entry(request, slug):
    """
    Detail view of each wiki entry
    """
    markdowner = Markdown()

    context = {
        "entry_title": slug,
        "entry_content": markdowner.convert(util.get_entry(slug))
    }

    return render(request, "encyclopedia/entry.html", context)


def create(request):
    """
    Create wiki entries
    """

    if request.method == 'GET':
        return render(request, "encyclopedia/create.html")

    elif request.method == 'POST':
        entry_title = request.POST.get('entry_title')
        entry_content = request.POST.get('entry_content')

        entries = util.list_entries()

        if entry_title in entries:
            context = {
                "error": "Title already exists"
            }
        else:
            context = {
                "error": None,
            }
            # Now save the title and content to /entries folder as .md Markdown file
            util.save_entry(entry_title, entry_content)

        return render(request, "encyclopedia/create.html", context)


def edit(request,slug):
    """
    Edit wiki entry
    """

    if request.method == 'GET':
        context = {
            "entry_title": slug,
            "entry_content": util.get_entry(slug)
        }
        return render(request, "encyclopedia/edit.html", context)

    elif request.method == 'POST':
        entry_content = request.POST.get('entry_content') #get the new content
        util.save_entry(slug, entry_content) #save the new content

        return redirect('/wiki/'+slug)


def random(request):
    entries = util.list_entries()
    slug = rdm.choice(entries)
    return redirect('/wiki/'+slug)
