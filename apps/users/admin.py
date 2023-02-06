from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from .models import User

# Register your models here.
class UserAdminConfig(UserAdmin):
    model = User
    search_fields = ('email', 'name')
    list_filter = ('country', 'contract_type', 'is_active')
    list_display = ('email', 'name', 'country', 'contract_type', 'is_active')
    ordering = ('name',)

    fieldsets = (
        (None, {'fields': ('email', 'name')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('Personal', {'fields': ('country', 'contract_type', 'password')})
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'country', 'contract_type', 'password1', 'password2', 'is_active', 'is_staff', 'is_superuser')
        }),
    )

admin.site.register(User, UserAdminConfig)
admin.site.unregister(Group) # Hide the Groups model from the admin site

admin.site.site_header = 'Timesheet administration panel' # Change the header of the Django admin site
admin.site.index_title = 'Timesheet' # Change the index title of the Django admin site
admin.site.site_title = ' ' # Change the title of the Django admin site