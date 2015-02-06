from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('frontend.views',
    # Examples:
    url(r'^create/$', 'create'),
    url(r'^stop_time/$', 'stop_time', name='stop_time'),
    url(r'^save/$', 'save', name='save'),
    url(r'^delete_task/$', 'action'),

    url(r'^$', 'index', name='index'),
    url(r'^.*$', 'index', name='default'),
    # url(r'^niezapominka/', include('niezapominka.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
