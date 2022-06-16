import math
from datetime import datetime

from colorfield.fields import ColorField
from django.contrib.auth.models import User
from django.db import models
from ckeditor.fields import RichTextField
from phonenumber_field.formfields import PhoneNumberField


class Advantages(models.Model):
    image = models.FileField(upload_to='gallery_images', null=True, blank=True, verbose_name='Фото')
    header = models.CharField(max_length=200, verbose_name='Заголовок')
    description = RichTextField(max_length=200, verbose_name='Описание')

    class Meta:
        verbose_name_plural = "Преимущества"
        verbose_name = 'Преимущество'

    def __str__(self):
        return self.header


class Image(models.Model):
    image = models.FileField(upload_to='gallery_images')
    about_us = models.ForeignKey('About_us', related_name='images', on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name_plural = 'Фото для главы "О нас"'
        verbose_name = 'Фото для главы "О нас"'

    def __str__(self):
        return 'Фото для главы "О нас"'


class ImageForItem(models.Model):
    image = models.FileField(upload_to='gallery_images')
    color = ColorField(null=True, blank=True)
    item = models.ForeignKey('Item', related_name='images_for_item', on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name_plural = 'Фото для товара'
        verbose_name = 'Фото для товара'



class About_us(models.Model):
    header = models.CharField(max_length=200, verbose_name='Заголовок')
    description = RichTextField(max_length=1000, verbose_name='Описание')

    class Meta:
        verbose_name_plural = "О нас"
        verbose_name = "О нас"

    def __str__(self):
        return self.header


class Help(models.Model):
    questions = models.CharField(max_length=200, verbose_name='Вопросы')
    answers = RichTextField(max_length=1000, verbose_name='Ответы')

    class Meta:
        verbose_name_plural = "Помощь"
        verbose_name = "Помощь"

    def __str__(self):
        return self.questions


class ImageHelp(models.Model):
    image = models.FileField(upload_to='gallery_images', null=True, verbose_name='Фото для вопросов')

    class Meta:
        verbose_name_plural = 'Фото для главы "Помощь"'
        verbose_name = 'Фото для главы "Помощь"'

    def save(self, *args, **kwargs):
        self.pk = 1
        super(ImageHelp, self).save(*args, **kwargs)

    def __str__(self):
        return self.image.url


class News(models.Model):
    image = models.FileField(upload_to='gallery_images', null=True, verbose_name='Фото для новостей')
    title = models.CharField(max_length=200, verbose_name='Название')
    description = RichTextField(max_length=1000, verbose_name='Описание')

    class Meta:
        verbose_name_plural = "Новости"
        verbose_name = "Новость"

    def __str__(self):
        return self.title


class Collection(models.Model):
    image = models.FileField(upload_to='gallery_images', null=True, verbose_name='Фото коллекции')
    title = models.CharField(max_length=200, verbose_name='Название')

    class Meta:
        verbose_name_plural = "Коллекции"
        verbose_name = "Коллекция"

    def __str__(self):
        return self.title


class Item(models.Model):
    collection = models.ForeignKey('Collection', on_delete=models.CASCADE, related_name='items_collection', null=True, blank=True)
    title = models.CharField(max_length=200, verbose_name='Название', blank=True)
    article = models.CharField(max_length=200, verbose_name='Артикул', null=True, blank=True)
    price = models.IntegerField(verbose_name='Цена', null=True, blank=True)
    old_price = models.IntegerField(verbose_name='Старая цена', null=True, blank=True)
    discount = models.IntegerField(verbose_name='Процент скидки', null=True, blank=True)
    description = RichTextField(max_length=1000, verbose_name='Описание товара', null=True, blank=True)
    product_size = models.CharField(max_length=200, verbose_name='Размерный ряд товара', null=True, blank=True)
    fabric_structure = models.CharField(max_length=200, verbose_name='Состав ткани', null=True, blank=True)
    quantity_in_line = models.IntegerField(verbose_name='Количество в линейке', null=True, blank=True)
    material = models.CharField(max_length=200, verbose_name='Материал', null=True, blank=True)
    hit_of_sales = models.BooleanField(default=False)
    new_product = models.BooleanField(default=False)
    favorite = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Товары"
        verbose_name = "Товар"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.discount:
            self.old_price = int(self.price) * (100 - int(self.discount)) / 100
        else:
            self.old_price = None
        super(Item, self).save(*args, **kwargs)


class Public_offer(models.Model):
    header = models.CharField(max_length=200, verbose_name='Заголовок')
    description = RichTextField(max_length=1000, verbose_name='Описание')

    class Meta:
        verbose_name_plural = 'Публичная оферта'
        verbose_name = 'Публичная оферта'

    def __str__(self):
        return self.header


class Slider(models.Model):
    image = models.FileField(upload_to='gallery_images', null=True, verbose_name='Фото для слайдера')
    title = models.CharField(max_length=200, verbose_name='Название', null=False, blank=False)

    class Meta:
        verbose_name_plural = "Слайдеры"
        verbose_name = "Слайдер"

    def __str__(self):
        return self.title


class Call_back(models.Model):
    name = models.CharField(max_length=200, verbose_name='Имя', blank=False, null=False)
    phone = models.CharField(max_length=200, verbose_name='Номер телефона', blank=False, null=False)
    date = models.DateTimeField(verbose_name='Дата обращения', blank=False, null=False)
    call_type = models.CharField(max_length=200, verbose_name='Тип обращения', blank=False, null=False)
    status = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'Обратный звонок'
        verbose_name = 'Обратный звонок'

    def __str__(self):
        return self.name


STATUS_OF_ORDER = [
    ('Новый', 'Новый'),
    ('Оформлен', 'Оформлен'),
    ('Отменен', 'Отменен')
]


class Order(models.Model):
    name = models.CharField(max_length=200, verbose_name='Имя', blank=False, null=True)
    surname = models.CharField(max_length=200, verbose_name='Фамилия', blank=False, null=True)
    email = models.CharField(max_length=200, verbose_name='Email', blank=False, null=True)
    phone = models.CharField(max_length=20, verbose_name='Телефон', blank=False, null=True)
    country = models.CharField(max_length=200, verbose_name='Страна', blank=False, null=True)
    city = models.CharField(max_length=200, verbose_name='Город', blank=False, null=True)

    class Meta:
        verbose_name = 'Заказы'
        verbose_name_plural = 'Заказ'


class BasketOrder(models.Model):
    image = models.FileField(upload_to='gallery_images', null=True, verbose_name='Фото для заказа товара')
    color = ColorField(null=True, blank=True)
    title = models.CharField(max_length=50, null=True, blank=True)
    size = models.CharField(max_length=10, null=True, blank=True)
    price = models.IntegerField(null=True, blank=True)
    old_price = models.IntegerField(null=True, blank=True)
    discount = models.IntegerField(null=True, blank=True)
    quantity_in_line = models.CharField(verbose_name='Размеры в линейке', null=True, blank=True, max_length=10)
    total_lines = models.IntegerField(null=True, blank=True, verbose_name='Количество линеек')
    total_products = models.IntegerField(null=True, blank=True, verbose_name='Количество всех товаров')
    total_price = models.IntegerField(null=True, blank=True, verbose_name='Стоимость всех линеек')
    total_discount = models.IntegerField(null=True, blank=True, verbose_name='Скидка от всей суммы')
    total_payment = models.IntegerField(null=True, blank=True, verbose_name='Итого к оплате')
    basket = models.ForeignKey('Order', on_delete=models.CASCADE, related_name='orders_basket', null=True)
    status = models.CharField(max_length=50, choices=STATUS_OF_ORDER, default='new')
    data = models.DateField(null=False, default=datetime.today)

    class Meta:
        verbose_name = 'Товары в корзинке'
        verbose_name_plural = 'Товары в корзинке'

    def save(self, *args, **kwargs):
        list_of_quantity = list(self.quantity_in_line.split("-"))
        sizes = math.ceil(((int(list_of_quantity[1]) - int(list_of_quantity[0])) / 2) + 1)
        self.total_products = sizes * int(self.total_lines)
        if self.old_price:
            self.total_price = int(self.total_products) * int(self.price)
            self.total_discount = int(self.total_price) - ((int(self.total_products) * int(self.old_price)))
            self.total_payment = int(self.total_price) - int(self.total_discount)
        else:
            self.total_price = int(self.total_products) * int(self.price)
            self.total_payment = self.total_price
        super(BasketOrder, self).save(*args, **kwargs)


