from django.contrib import admin
from .models import CustomUsers
from django.contrib.auth.admin import UserAdmin

# Register your models here.

class ModelAdmin(UserAdmin):
    model = CustomUsers
    list_display = ('username', 'email', 'is_staff', 'date_of_birth')
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('date_of_birth', 'profile_photo')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('date_of_birth', 'profile_photo')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )

admin.site.register(CustomUsers, ModelAdmin)