# -*- coding: utf-8 -*-
from django.shortcuts import render, render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.template.context import RequestContext

from django.contrib import auth
from django.contrib.auth.views import login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache

from django.core.mail import send_mail
from django import forms

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

import datetime

from books.models import Book, Record, HistoryRecord
from books.forms import UserCreateForm

# Create your views here.
@never_cache
def index(request):
    user = request.user
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
        RequestContext(request, {'books': books, 'user': user, }))

@never_cache
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

@never_cache
def login(request):
    return auth.views.login(request, template_name='books/login.html')


@login_required
@never_cache
def logout(request):
    auth.views.logout(request, \
        template_name='books/logout.html') 
    return HttpResponseRedirect('/books/')


@login_required
@never_cache
def borrow(request, bookid):
    book = Book.objects.get(identifier=bookid)
    book.status = '已借出'
    book.save()
    user = request.user
    sdate = datetime.datetime.today().date()
    edate = sdate + datetime.timedelta(days=31)

    record = Record(book=book, user=user, sdate=sdate, edate=edate, count=2)
    record.save()

    url_redirect = '/accounts/profile/%s/' % user.username
    records = user.record_set.all()
    return HttpResponseRedirect(url_redirect, \
        RequestContext(request, {'user': user, 'records': records, })) 

@login_required
@never_cache
def renew(request, bookid):
    book = Book.objects.get(identifier=bookid)
    record = book.record
    today = datetime.datetime.today().date()
    edate = today + datetime.timedelta(days=16)
    record.edate = edate
    record.count = record.count - 1
    record.save()
    user = request.user
    records = user.record_set.all()
    url_redirect = '/accounts/profile/%s/' % user.username
    return HttpResponseRedirect(url_redirect, \
        RequestContext(request, {'user': user, 'records': records, }))
    
@login_required
@never_cache
def bookreturn(request, bookid):
    book = Book.objects.get(identifier=bookid)
    record = book.record
    user = record.user
    sdate = record.sdate
    edate = datetime.datetime.today().date()
    record.delete()
    book.status = "在架可借"
    book.save()
    records = user.record_set.all()
    url_redirect = '/accounts/profile/%s/' % user.username
    return HttpResponseRedirect(url_redirect, \
        RequestContext(request, {'user': user, 'records': records, }))

@never_cache
def bookinfo(request, bookid):
    book = Book.objects.get(identifier=bookid)
    return render_to_response('books/bookinfo.html', \
        RequestContext(request, {'book': book, }))

@login_required
@never_cache
def userinfo(request, username):
    user = User.objects.get(username=username)
    records = user.record_set.all()
    return render_to_response('books/userinfo.html', \
        RequestContext(request, {'user': user, 'records': records, }))

#def profile(request):
#    user = request.user
#    records = user.record_set.all()
#    return render_to_response('/books/userinfo.html', \
#        RequestContext(request, {'user': user, 'records': records, }))

@login_required
def changepasswd(request):
    pass

@never_cache
def search(request):
    searchtype = request.GET.get('searchtype')
    searchword = request.GET.get('searchword')
    if searchword != '':
        if searchtype == u"书名":
            book_list = Book.objects.filter(name__contains=searchword)
        if searchtype == u"作者":
            book_list = Book.objects.filter(author__contains=searchword)
        if searchtype == u"出版社":
            book_list = Book.objects.filter(publisher__contains=searchword)
        if searchtype == u"ID":
            book_list = Book.objects.filter(identifier__contains=searchword)
    
        paginator = Paginator(book_list, 10) # show 10 books per page

        page = request.GET.get('page')
        try:
            books = paginator.page(page)
        except PageNotAnInteger:
            books = paginator.page(1)
        except EmptyPage:
            books = paginator.page(paginator.num_pages)
        user = request.user
        return render_to_response('books/searchresults.html', \
            RequestContext(request, {'book_list': book_list, 'books': books, 'user': user, \
                'searchtype': searchtype, 'searchword': searchword, }))
    else:
        user = request.user
        book_list = Book.objects.all()
        paginator = Paginator(book_list, 10) # show 10 books per page

        page = request.GET.get('page')
        try:
            books = paginator.page(page)
        except PageNotAnInteger:
            books = paginator.page(1)
        except EmptyPage:
            books = paginator.page(paginator.num_pages)
        return HttpResponseRedirect('/books/', \
            RequestContext(request, {'books': books, 'user': user, }))
        
