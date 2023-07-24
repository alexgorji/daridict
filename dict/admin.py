from django.contrib import admin

# Register your models here.
from .models import DictItem, DictLanguage, DictEntry

admin.site.register(DictItem)
admin.site.register(DictLanguage)
admin.site.register(DictEntry)

