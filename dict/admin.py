from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin

# Register your models here.
from .models import DictItem, DictLanguage, DictEntry, DictSource, Tag


class DictEntryHistoryAdmin(SimpleHistoryAdmin):
    history_list_display = ["approved", "tags"]

admin.site.register(DictItem, SimpleHistoryAdmin)
admin.site.register(DictLanguage, SimpleHistoryAdmin)
admin.site.register(DictEntry, DictEntryHistoryAdmin)
admin.site.register(DictSource, SimpleHistoryAdmin)
admin.site.register(Tag, SimpleHistoryAdmin)
