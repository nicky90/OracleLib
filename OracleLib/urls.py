from django.conf.urls import patterns, include, url

import books

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'OracleLib.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/register/$', 'books.views.register', name='register'),
    url(r'^accounts/login/$', 'books.views.login', name='login'),
    url(r'^accounts/logout/$', 'books.views.logout', name='logout'),
    url(r'^accounts/profile/(?P<username>\w+)/$', 'books.views.userinfo', name='userinfo'),
    url(r'^books/', include('books.urls', namespace='books')),
)
