import nested_admin
from django.contrib.admin import TabularInline
from nested_admin import nested
from django.contrib import admin
from webapp.models import Advantages, Image, About_us, Help, ImageHelp, News, Collection, Item, ImageForItem


class AdvantagesAdmin(admin.ModelAdmin):
    list_display = ['image', 'header', 'description']


class ImageAdminInline(TabularInline):
    extra = 1
    model = ImageForItem


@admin.register(Item)
class ProductModelAdmin(admin.ModelAdmin):
    inlines = (ImageAdminInline,)
    exclude = []


admin.site.register(Advantages)
admin.site.register(ImageHelp)
admin.site.register(Help)
admin.site.register(Image)
admin.site.register(About_us)
admin.site.register(News)
admin.site.register(Collection)
