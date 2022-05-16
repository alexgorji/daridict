from pprint import pprint

from django.contrib import admin

# Register your models here.
from .models import DictItem, DictLanguage, DictNode

admin.site.register(DictItem)
admin.site.register(DictLanguage)
admin.site.register(DictNode)
