from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from django.core.urlresolvers import reverse_lazy

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mydjango_project.views.home', name='home'),
    # url(r'^mydjango_project/', include('mydjango_project.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    # Your project url
    url(r'^', include('apps.bookmarks.urls',
                       namespace='bookmarks',
                       app_name='bookmarks')),
    url(r'^users/', include('apps.users.urls',
                            namespace='users',
                            app_name='users')),
    url(r'^friend/', include('apps.friends.urls',
                             namespace='friends',
                             app_name='friends')),
)
