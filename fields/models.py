from django.db import models
from core.models import User
from core.models import LandLord
from slugify import slugify



class Field(models.Model):
    name = models.CharField(max_length=1024)
    description = models.TextField(null=True, blank=True)
    owner = models.ForeignKey(LandLord, null=True, blank=True, on_delete=models.CASCADE)
    area = models.CharField(max_length=255, null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)



class Image(models.Model):
    field = models.ForeignKey(Field, null=True, blank=True, default=None, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='uploads/', verbose_name='Image')

