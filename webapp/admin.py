from django.contrib import admin
from webapp.models import Advantages, Image, About_us


class AdvantagesAdmin(admin.ModelAdmin):
    list_display = ['image', 'header', 'description']


admin.site.register(Advantages)
admin.site.register(Image)
admin.site.register(About_us)
