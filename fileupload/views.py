import random
import logging
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest
from fileupload.models import MultiuploaderImage
from django.core.files.uploadedfile import UploadedFile
from django.views.decorators.csrf import csrf_exempt
from django.utils import simplejson
from django.core.urlresolvers import reverse

#for generating thumbnails
#sorl-thumbnails must be installed and properly configured
#from sorl.thumbnail import get_thumbnail


log = logging


def key_generate():
    """returns a string based unique key with length 80 chars"""
    while 1:
        key = str(random.getrandbits(40))
        try:
            MultiuploaderImage.objects.get(key=key)
        except:
            return key

@csrf_exempt
def multiuploader_delete(request, pk):
    if request.user.is_authenticated() == False: return HttpResponseBadRequest('Not authenticated')

    if request.method == 'POST':
        image = get_object_or_404(MultiuploaderImage, pk=pk)
        image.image.delete()
        image.delete()

        return HttpResponse(str(pk))
    else:
        log.info('Received not POST request to delete image view')
        return HttpResponseBadRequest('Only POST accepted')

@csrf_exempt
def multiuploader(request):
    """
    Main Multiuploader module.
    Parses data from jQuery plugin and makes database changes.
    """
    if request.user.is_authenticated() == False: return HttpResponseBadRequest('Not authenticated')

    if request.method == 'GET':
        result = []

        images = MultiuploaderImage.objects.filter(user=request.user)


        for image in images:
            wrapped_file = UploadedFile(image.image)
            result.append({"name":str(image.key_data),
                           "size":wrapped_file.file.size,
                           "url":settings.MEDIA_URL+image.image.name,
                           "thumbnail_url":settings.MEDIA_URL+image.image.name,
                           "delete_url": reverse('deleter', args=(image.id,)),
                           "delete_type":"POST",})

        response_data = simplejson.dumps(result)

        if "application/json" in request.META['HTTP_ACCEPT_ENCODING']:
            mimetype = 'application/json'
        else:
            mimetype = 'text/plain'
        return HttpResponse(response_data, mimetype=mimetype)

    if request.method == 'POST':
        log.info('received POST to main multiuploader view')
        if request.FILES == None:
            return HttpResponseBadRequest('Must have files attached!')


        file = request.FILES.get('file')
        file.name = key_generate() + ".jpg"
        wrapped_file = UploadedFile(file)


        image = MultiuploaderImage()
        image.image = file
        image.key_data = file.name
        image.user = request.user
        image.save()


        result = []
        result.append({"name":str(image.key_data),
                       "size":wrapped_file.file.size,
                       "url":settings.MEDIA_URL+image.image.name,
                       "thumbnail_url":settings.MEDIA_URL+image.image.name,
                       "delete_url":reverse('deleter', args=(image.id,)),
                       "delete_type":"POST",})
        response_data = simplejson.dumps(result)

        if "application/json" in request.META['HTTP_ACCEPT_ENCODING']:
            mimetype = 'application/json'
        else:
            mimetype = 'text/plain'
        return HttpResponse(response_data, mimetype=mimetype)
    else:
        return HttpResponse('Only POST\GET accepted')
