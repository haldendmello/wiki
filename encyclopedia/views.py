from django.shortcuts import render,redirect,reverse
import random,os
from . import util
import markdown as md
from django.http import request, HttpResponse, HttpResponseRedirect,HttpResponseNotFound
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.contrib import messages

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def create(request):
    if request.method == 'GET' :
        return render(request,"encyclopedia/create.html")
    else:
        title = request.POST["title"]
        content = request.POST["content"]
        filename = f"entries/{title}.md"
        if default_storage.exists(filename):
            messages.error(request,"File Already Exist",extra_tags='danger')
            return HttpResponseRedirect(reverse('index'))
        default_storage.save(filename, ContentFile(content))
        messages.success(request,"File Created Successfully",extra_tags='success')
        return HttpResponseRedirect(reverse('index'))


def edit(request,title):
    
    if request.method == 'GET' :
        f = default_storage.open(f"entries/{title}.md")
        context={
            'title' : title,
            'mdcontent' : f.read().decode("utf-8")
        }
        return render(request,"encyclopedia/edit.html", context)

def edited(request,title):
    content = request.POST["mdcontent"]
    util.save_entry(title, content)
    return HttpResponseRedirect(reverse('wiki', args=(title,)))

def search(request):
    search = request.GET["q"]
    entries = util.list_entries()
    result = []

    if search in entries :
        return HttpResponseRedirect(reverse('wiki', args=(search,)))
    else:
        for i in range(len(entries)):
            if search in entries[i].lower():
                result.append(entries[i])
        
    context = {
        'entries' : result 
    }
    return render(request,"encyclopedia/search.html",context)

def randome(request):
    titles = util.list_entries()
    title = random.choice(titles)
    return HttpResponseRedirect(reverse('wiki', args=(title,)))