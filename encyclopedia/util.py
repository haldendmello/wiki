import re

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage

import markdown as md

from django.http import request, HttpResponse, HttpResponseRedirect,HttpResponseNotFound

from django.shortcuts import render,reverse



def list_entries():
    """
    Returns a list of all names of encyclopedia entries.
    """
    _, filenames = default_storage.listdir("entries")
    return list(sorted(re.sub(r"\.md$", "", filename)
                for filename in filenames if filename.endswith(".md")))


def save_entry(title, content):
    """
    Saves an encyclopedia entry, given its title and Markdown
    content. If an existing entry with the same title already exists,
    it is replaced.
    """
    filename = f"entries/{title}.md"
    if default_storage.exists(filename):
        default_storage.delete(filename)
    default_storage.save(filename, ContentFile(content))
    


def get_entry(request,title):
    """
    Retrieves an encyclopedia entry by its title. If no such
    entry exists, the function returns None.
    """
    try:
        f = default_storage.open(f"entries/{title}.md")
        context = {
            'mdcontent' : md.markdown(f.read().decode("utf-8")),
            'title' : title 
        }
        return render(request,"encyclopedia/view.html" , context )
    except FileNotFoundError:
        return HttpResponseNotFound('<h1>Page not found</h1>')


    



