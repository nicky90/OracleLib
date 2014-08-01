# -*- coding: utf-8 -*-
from django.shortcuts import render, render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.template.context import RequestContext

from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required

from django.core.mail import send_mail
from django import forms

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from books.models import Book
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
        RequestContext(request, {'books': books,}))
