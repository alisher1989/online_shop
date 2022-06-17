from django.contrib.admin import TabularInline
from django.contrib import admin
from django.utils.safestring import mark_safe

from webapp.models import Advantages, Image, About_us, Help, ImageHelp, News, Collection, Item, ImageForItem, \
    Public_offer, Slider, Call_back, Order, BasketOrder


class AdvantagesAdmin(admin.ModelAdmin):
    list_display = ['image', 'header', 'description']


class ImageAdminInline(TabularInline):
    extra = 1
    model = ImageForItem
    fields = ['image', 'color']


@admin.register(Item)
class ProductModelAdmin(admin.ModelAdmin):
    inlines = (ImageAdminInline,)
    exclude = ['order']


class CityTabularInline(TabularInline):
    model = BasketOrder
    extra = 1


class OrderAdmin(admin.ModelAdmin):
    inlines = [CityTabularInline, ]
    search_fields = ['phone', 'name', 'surname', 'email']


admin.site.register(Order, OrderAdmin)
admin.site.register(Advantages)
admin.site.register(ImageHelp)
admin.site.register(Help)
admin.site.register(Image)
admin.site.register(About_us)
admin.site.register(News)
admin.site.register(Collection)
admin.site.register(Public_offer)
admin.site.register(Slider)
admin.site.register(Call_back)