from django.conf.urls import patterns, url

import books

urlpatterns = patterns('books.views',
    url(r'^$', 'index', name='index'),
    url(r'^profile/(?P<bookid>[-A-Z0-9]+)/$', 'bookinfo', name='bookinfo'),
    url(r'^borrow/(?P<bookid>\w+)/$', 'borrow', name='borrow'),
)

