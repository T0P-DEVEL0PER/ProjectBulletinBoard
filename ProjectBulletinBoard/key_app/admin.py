from django.contrib import admin
from .models import *

admin.site.register(Category)
admin.site.register(Advertisement)
admin.site.register(Reply)
admin.site.register(OneTimeCode)
