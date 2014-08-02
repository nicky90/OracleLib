# -*- coding: utf-8 -*-
from django.shortcuts import render, render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.template.context import RequestContext

from django.contrib import auth
from django.contrib.auth.views import login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from django.core.mail import send_mail
from django import forms

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from books.models import Book
from books.forms import UserCreateForm

# Create your views here.
def index(request):
    book_list = Book.objects.all()
    paginator = Paginator(book_list, 10) # show 10 books per page

    page = request.GET.get('page')
    try:
        books = paginator.page(page)
    except PageNotAnInteger:
        books = paginator.page(1)
    except EmptyPage:
        books = paginator.page(paginator.num_pages)
    return render_to_response('books/index.html', \
        RequestContext(request, {'books': books, }))


def register(request):
    if request.method == 'POST':
        form = UserCreateForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            return HttpResponseRedirect('/books/')
    else:
        form = UserCreateForm()
    return render_to_response('books/register.html', \
        RequestContext(request, {'form': form, }))

def login(request):
    return auth.views.login(request, \
        template_name='books/login.html')

@login_required
def logout(request):
    auth.views.logout(request, \
        template_name='books/logout.html') 
    return HttpResponseRedirect('/books/')

def borrow(request):
    pass

def bookinfo(request, bookid):
    book = Book.objects.get(identifier=bookid)
    return render_to_response('books/bookinfo.html', \
        RequestContext(request, {'book': book, }))


def profile(request):
    pass
