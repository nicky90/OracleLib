from django.conf.urls import patterns, url

import books

urlpatterns = patterns('books.views',
    url(r'^$', 'index', name='index'),
    url(r'^profile/(?P<bookid>[-A-Z0-9]+)/$', 'bookinfo', name='bookinfo'),
    url(r'^borrow/(?P<bookid>[-A-Z0-9]+)/$', 'borrow', name='borrow'),
    url(r'^return/(?P<bookid>[-A-Z0-9]+)/$', 'bookreturn', name='bookreturn'),
    url(r'^renew/(?P<bookid>[-A-Z0-9]+)/$', 'renew', name='renew'),
    url(r'^searchresults/$', 'search', name='search'),
)

