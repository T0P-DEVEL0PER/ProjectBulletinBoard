from ckeditor.widgets import CKEditorWidget
from django.contrib import admin
from .models import *

class AdvertisementAdmin(admin.ModelAdmin):
    formfield_overrides = {models.TextField: {'widget': CKEditorWidget}}

admin.site.register(Category)
admin.site.register(Advertisement, AdvertisementAdmin)
admin.site.register(Reply)
admin.site.register(OneTimeCode)
