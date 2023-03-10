from django.contrib import admin
from .models import Task, Occupation, UserTask
from ..users.models import User

# Register your models here.
class TaskAdminConfig(admin.ModelAdmin):
    model = Task
    search_fields = ('code', 'name')
    list_filter = ('is_active',)
    list_display = ('code', 'name', 'is_active')
    ordering = ('code',)

class OccupationAdminConfig(admin.ModelAdmin):
    model = Occupation
    list_display = ('users', 'tasks', 'date', 'start_time', 'end_time', 'description')
    ordering = ('-users', '-date', '-start_time')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'users':
            kwargs['queryset'] = User.objects.filter(is_active=True)
        
        if db_field.name == 'tasks':
            kwargs['queryset'] = Task.objects.filter(is_active=True)
        
        return super(OccupationAdminConfig, self).formfield_for_foreignkey(db_field, request, **kwargs)

class UserTaskAdminConfig(admin.ModelAdmin):
    model = UserTask
    list_filter = ('tasks', 'is_active')
    list_display = ('users', 'tasks', 'is_active')
    ordering = ('-users', 'tasks')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'users':
            kwargs['queryset'] = User.objects.filter(is_active=True)
        
        if db_field.name == 'tasks':
            kwargs['queryset'] = Task.objects.filter(is_active=True)
        
        return super(UserTaskAdminConfig, self).formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(Task, TaskAdminConfig)
admin.site.register(Occupation, OccupationAdminConfig)
admin.site.register(UserTask, UserTaskAdminConfig)