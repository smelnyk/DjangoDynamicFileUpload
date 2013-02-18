from django.conf.urls import patterns, include, url
from django.conf import settings
from django.views.generic import TemplateView
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^upload/', include('fileupload.urls')),
    url(r'^$', TemplateView.as_view(template_name="fileupload_example.html"), name="example"),
)

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += patterns('',
        (r'media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': './media/'}),
    )
