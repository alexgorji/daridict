# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import MyUser


class MyUserAdmin(UserAdmin):
    add_form_template = 'admin/add_form.html'
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2'),
        }),
    )


# admin.site.register(MyUser, MyUserAdmin)
admin.site.register(MyUser)
