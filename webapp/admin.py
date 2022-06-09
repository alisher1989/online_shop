import nested_admin
from nested_admin import nested
from django.contrib import admin
from webapp.models import Advantages, Image, About_us, Help, ImageHelp, News, Collection


class AdvantagesAdmin(admin.ModelAdmin):
    list_display = ['image', 'header', 'description']


admin.site.register(Advantages)
admin.site.register(ImageHelp)
admin.site.register(Help)
admin.site.register(Image)
admin.site.register(About_us)
admin.site.register(News)
admin.site.register(Collection)
