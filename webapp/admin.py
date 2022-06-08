from django.contrib import admin
from webapp.models import Advantages


class AdvantagesAdmin(admin.ModelAdmin):
    list_display = ['image', 'header', 'description']


admin.site.register(Advantages)
