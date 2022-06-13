from django.contrib.admin import TabularInline
from django.contrib import admin

from webapp.models import Advantages, Image, About_us, Help, ImageHelp, News, Collection, Item, ImageForItem


class AdvantagesAdmin(admin.ModelAdmin):
    list_display = ['image', 'header', 'description']


class ImageAdminInline(TabularInline):
    extra = 1
    model = ImageForItem
    fields = ['image', 'color']

    #def has_add_permission(self, request, obj):
     #   if obj.images_for_item.count() >= 2:
      #      return False
       # print(dir(obj))
        #print(type(obj))
       # return True


#class HomePageModelForm(forms.ModelForm):
#    def clean(self):
#        if self.instance.images_for_item.all().count() > 2:
#            self._errors.setdefault('__all__', ErrorList()).append("Вы не можете добавлять больше 3 фото на один товар.")
#        return self.cleaned_data


@admin.register(Item)
class ProductModelAdmin(admin.ModelAdmin):
#    form = HomePageModelForm
    inlines = (ImageAdminInline,)
    exclude = []


admin.site.register(Advantages)
admin.site.register(ImageHelp)
admin.site.register(Help)
admin.site.register(Image)
admin.site.register(About_us)
admin.site.register(News)
admin.site.register(Collection)
