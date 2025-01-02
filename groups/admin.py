from django.contrib import admin
from .models import Groups, GroupMembership

# Register your models here.
class GroupsAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'budget',
        'created_at',
        'updated_at',
    )

admin.site.register(Groups, GroupsAdmin)

admin.site.register(GroupMembership)