from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CheetahUser

class CheetahUserAdmin(UserAdmin):
    list_display = ('email', 'name', 'mobile_number_with_country_code', 'is_active', 'is_staff')
    list_filter = ('is_active', 'is_staff',)
    search_fields = ('email', 'name', 'mobile_number_with_country_code',)
    ordering = ('email',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('name', 'mobile_number_with_country_code')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', )}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'mobile_number_with_country_code', 'password1', 'password2', 'is_active', 'is_staff')}
        ),
    )

admin.site.register(CheetahUser, CheetahUserAdmin)
