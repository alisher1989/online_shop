from django.db import models
from ckeditor.fields import RichTextField


class Advantages(models.Model):
    image = models.FileField(upload_to='gallery_images', null=True, blank=True, verbose_name='Фото')
    header = models.CharField(max_length=200, verbose_name='Заголовок')
    description = RichTextField(max_length=200, verbose_name='Описание')

    def __str__(self):
        return self.header


class Image(models.Model):
    image = models.FileField(upload_to='gallery_images')
    about_us = models.ForeignKey('About_us', related_name='images', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.about_us


class About_us(models.Model):
    #image = models.ForeignKey('Image', on_delete=models.CASCADE)
    header = models.CharField(max_length=200, verbose_name='Заголовок')
    description = RichTextField(max_length=1000, verbose_name='Описание')

    def __str__(self):
        return self.header


