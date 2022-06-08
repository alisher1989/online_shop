from django.db import models


class Advantages(models.Model):
    image = models.ImageField(upload_to='gallery_images', null=True, blank=True, verbose_name='Фото')
    header = models.CharField(max_length=200, verbose_name='Заголовок')
    description = models.CharField(max_length=200, verbose_name='Описание')

    def __str__(self):
        return self.header
