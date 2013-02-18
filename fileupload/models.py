from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _



from django.conf import settings
try:
	storage = settings.MULTI_IMAGES_FOLDER+'/'
except AttributeError:
	storage = 'multiuploader_images/'

class MultiuploaderImage(models.Model):
	"""Model for storing uploaded photos"""
	image = models.FileField(upload_to=storage)
	key_data = models.CharField(max_length=20, unique=True)
	upload_date = models.DateTimeField(auto_now_add=True)
	user = models.ForeignKey(User)

	def __unicode__(self):
		return self.image.name