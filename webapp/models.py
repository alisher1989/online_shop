from django.db import models
from ckeditor.fields import RichTextField


class Advantages(models.Model):
    image = models.FileField(upload_to='gallery_images', null=True, blank=True, verbose_name='Фото')
    header = models.CharField(max_length=200, verbose_name='Заголовок')
    description = RichTextField(max_length=200, verbose_name='Описание')

    def __str__(self):
        return self.header


class Collection(models.Model):
    pass