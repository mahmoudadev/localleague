from django.db import models

class Field(models.Model):
    name = models.CharField(max_length=1024)
    description = models.TextField(null=True, blank=True)
    area = models.CharField(max_length=255, null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)



def get_image_filename(instance, filename):
    title = instance.post.title
    slug = slugify(title)
    return "post_images/%s-%s" % (slug, filename)



class Image(models.Model):
    field = models.ForeignKey(Field, null=True, blank=True, default=None, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=get_image_filename, verbose_name='Image')

