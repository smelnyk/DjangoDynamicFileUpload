from django.conf.urls.defaults import *


urlpatterns = patterns('',
	url(r'^delete/(\d+)/$', 'fileupload.views.multiuploader_delete', name='deleter'),
	url(r'^uploader/$', 'fileupload.views.multiuploader', name='uploader'),
)