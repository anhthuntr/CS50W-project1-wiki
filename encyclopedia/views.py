from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from random import choice
from django import forms
from . import util
import markdown


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request,name):
    entry = util.get_entry(name)
    if entry == None:
        return render(request,"encyclopedia/error.html", {
        })
    
    return render(request, "encyclopedia/entry.html", {
        "name" : name,
        "entry": markdown.markdown(entry)
    })

def search(request):
    query = request.GET.get('q','') 
    entries = util.list_entries()
    result = []

    for entry in entries:
        if query in entry.lower():  # Case-insensitive search
            result.append(entry)
    
    if query in entries:
        return redirect('entry', name=query)
    elif result:
        return render(request, "encyclopedia/search.html", {
            "entries": result
        })
    else:
        return render(request, "encyclopedia/error.html", {
            "message": f"No results found for '{query}'."
        })
    
def random(request):
    entries = util.list_entries()
    return redirect('entry', name=choice(entries))

def create(request):
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")
        existing_entries = [entry.lower() for entry in util.list_entries()]

        if title.lower() in existing_entries:
            return render(request, "encyclopedia/error.html", {
                "message": "Entry with this title already exists."
            })
        else:
            content = "#"+title+"\n"+content
            util.save_entry(title,content)
            return redirect('entry', name=title)
    else:
        return render(request,"encyclopedia/create.html")

def edit(request, name):
    if request.method == "POST":
        newContent = request.POST.get("content")
        newContent = "#"+name+"\n"+newContent
        util.save_entry(name,newContent)
        return redirect('entry', name=name)
    else:
        return render(request, "encyclopedia/edit.html",{
            "name": name,
            "content": util.get_entry(name)
        })
    



