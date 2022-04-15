from django.shortcuts import render
from . import models


def index(request):
    return render(request, 'blog/index.html')

def login(request):
    return render(request, 'blog/login.html')

def register(request):
    return render(request, 'blog/register.html')

def about(request):
    return render(request, 'blog/about.html')


def contact(request):
    return render(request, 'blog/contact.html')


def post(request, id):
    post = models.Post.objects.get(id=id)
    context = {"post": post}
    return render(request, 'blog/post.html', context)
