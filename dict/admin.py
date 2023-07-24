from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin

# Register your models here.
from .models import DictItem, DictLanguage, DictEntry

admin.site.register(DictItem, SimpleHistoryAdmin)
admin.site.register(DictLanguage, SimpleHistoryAdmin)
admin.site.register(DictEntry, SimpleHistoryAdmin)

