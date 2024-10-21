from django.contrib import admin
from dbbackup.management.commands.dbbackup import Command as DbBackupCommand
from django.utils.translation import gettext_lazy as _
from django.shortcuts import render

from .models import CustomUser

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('phone_number', 'email', 'full_name', 'is_staff', 'is_active', 'is_superuser')
    search_fields = ('phone_number', 'email', 'full_name')
    list_filter = ('is_staff', 'is_active')

    fieldsets = (
        (None, {
            'fields': ('phone_number', 'email', 'full_name')
        }),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser')
        }),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone_number', 'email', 'full_name', 'password1', 'password2', 'is_active', 'is_staff', 'is_superuser')}
        ),
    )
    
    def save_model(self, request, obj, form, change):
        if not change:
            obj.set_password(form.cleaned_data['password'])
        obj.save()


admin.site.register(CustomUser, CustomUserAdmin)