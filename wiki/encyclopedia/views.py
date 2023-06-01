from django.shortcuts import render, redirect
from django.urls import reverse
from markdown import markdown
import random

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def convert_md_to_html(title):
    content = util.get_entry(title)
    if content == None:
        return None
    else:
        return markdown(content)
    
def entry_display(request, title):
    entry_html = convert_md_to_html(title)
    if entry_html == None:
        return render(request, "encyclopedia/error.html", {
            "message": "This entry doesn't exist"
        })
    else:
        return render(request, "encyclopedia/entry_display.html", {
            "title": title,
            "content": entry_html
        })
    
def search(request):
    if request.method == "POST":
        searching = request.POST['q']
        content = convert_md_to_html(searching) ## convert title to the entry

        if content is not None:
            return render(request, "encyclopedia/entry_display.html", {
            "title": searching,
            "content": content
        })
        else:
            entries = []
            for entry in util.list_entries():
                if searching.lower() in entry.lower():
                    entries.append(entry)
            return render(request, "encyclopedia/search.html", {
                "entries": entries,
                "searching": searching
            })

def new_page(request):
    if request.method == "POST":
        title = request.POST['title']
        content = request.POST['content']

        if util.get_entry(title) == None:
            util.save_entry(title, content)
            return redirect(reverse('entry_display', args=[title]))
        else:
            return render(request, "encyclopedia/error.html", {
                'message': 'An entry with this title already exists'
            })
    else:
        return render(request, "encyclopedia/new_page.html")

def edit_page(request):
    if request.method == "POST":
        title = request.POST['title']
        content = util.get_entry(title)
        if content is None:
            return render(request, "encyclopedia/error.html", {
                "message": "This entry does not exist"
            })
        return render(request, "encyclopedia/edit_page.html", {
            'title': title,
            'content': content
        })
    
def save_edit(request):
    if request.method == 'POST':
        title = request.POST['title']
        content = request.POST['content']

        util.save_entry(title, content)
        new_content = convert_md_to_html(title)
        return render(request, "encyclopedia/entry_display.html", {
            'title': title,
            'content': new_content
        })

def random_page(request):
    entries = util.list_entries()
    random_title = random.choice(entries)
    return redirect('entry_display', title=random_title)


