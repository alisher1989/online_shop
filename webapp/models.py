from colorfield.fields import ColorField
from django.db import models
from ckeditor.fields import RichTextField


class Advantages(models.Model):
    image = models.FileField(upload_to='gallery_images', null=True, blank=True, verbose_name='Фото')
    header = models.CharField(max_length=200, verbose_name='Заголовок')
    description = RichTextField(max_length=200, verbose_name='Описание')

    class Meta:
        verbose_name_plural = "Преимущества"

    def __str__(self):
        return self.header


class Image(models.Model):
    image = models.FileField(upload_to='gallery_images')
    about_us = models.ForeignKey('About_us', related_name='images', on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name_plural = 'Фото для главы "О нас"'

    def __str__(self):
        return 'Фото для главы "О нас"'


class ImageForItem(models.Model):
    image = models.FileField(upload_to='gallery_images')
    color = ColorField(null=True, blank=True)
    item = models.ForeignKey('Item', related_name='images_for_item', on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name_plural = 'Фото для товара'

    def __str__(self):
        return 'Фото для товара'


class About_us(models.Model):
    header = models.CharField(max_length=200, verbose_name='Заголовок')
    description = RichTextField(max_length=1000, verbose_name='Описание')

    class Meta:
        verbose_name_plural = "О нас"

    def __str__(self):
        return self.header


class Help(models.Model):
    questions = models.CharField(max_length=200, verbose_name='Вопросы')
    answers = RichTextField(max_length=1000, verbose_name='Ответы')

    class Meta:
        verbose_name_plural = "Помощь"

    def __str__(self):
        return self.questions


class ImageHelp(models.Model):
    image = models.FileField(upload_to='gallery_images', null=True, verbose_name='Фото для вопросов')

    class Meta:
        verbose_name_plural = 'Фото для главы "Помощь"'

    def save(self, *args, **kwargs):
        self.pk = 1
        super(ImageHelp, self).save(*args, **kwargs)

    def __str__(self):
        return 'Фото для помощи'


class News(models.Model):
    image = models.FileField(upload_to='gallery_images', null=True, verbose_name='Фото для новостей')
    title = models.CharField(max_length=200, verbose_name='Название')
    description = RichTextField(max_length=1000, verbose_name='Описание')

    class Meta:
        verbose_name_plural = "Новости"

    def __str__(self):
        return self.title


class Collection(models.Model):
    image = models.FileField(upload_to='gallery_images', null=True, verbose_name='Фото коллекции')
    title = models.CharField(max_length=200, verbose_name='Название')

    class Meta:
        verbose_name_plural = "Коллекции"

    def __str__(self):
        return self.title


class Item(models.Model):
    collection = models.ForeignKey('Collection', on_delete=models.CASCADE, related_name='items_collection', null=True, blank=True)
    title = models.CharField(max_length=200, verbose_name='Название', blank=True)
    article = models.CharField(max_length=200, verbose_name='Артикул', null=True, blank=True)
    price = models.IntegerField(max_length=20, verbose_name='Цена', null=True, blank=True)
    old_price = models.IntegerField(max_length=20, verbose_name='Старая цена', null=True, blank=True)
    discount = models.IntegerField(max_length=20, verbose_name='Процент скидки', null=True, blank=True)
    description = RichTextField(max_length=1000, verbose_name='Описание товара', null=True, blank=True)
    product_size = models.CharField(max_length=200, verbose_name='Размерный ряд товара', null=True, blank=True)
    fabric_structure = models.CharField(max_length=200, verbose_name='Состав ткани', null=True, blank=True)
    quantity_in_line = models.IntegerField(max_length=20, verbose_name='Количество в линейке', null=True, blank=True)
    material = models.CharField(max_length=200, verbose_name='Материал', null=True, blank=True)
    hit_of_sales = models.BooleanField(default=False)
    new_product = models.BooleanField(default=False)
    favorite = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Товары"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.discount:
            Discount_Amount = (self.discount * self.price) / 100
            Discounted_Price = self.price - Discount_Amount
            self.old_price = Discounted_Price
        else:
            self.old_price = None
        super(Item, self).save(*args, **kwargs)


class Public_offer(models.Model):
    header = models.CharField(max_length=200, verbose_name='Заголовок')
    description = RichTextField(max_length=1000, verbose_name='Описание')

    class Meta:
        verbose_name_plural = 'Публичная оферта'


class Slider(models.Model):
    image = models.FileField(upload_to='gallery_images', null=True, verbose_name='Фото для слайдера')
    title = models.CharField(max_length=200, verbose_name='Название', null=False, blank=False)

    class Meta:
        verbose_name_plural = "Слайдеры"





