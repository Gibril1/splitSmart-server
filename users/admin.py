from django.contrib import admin
from .models import User


class UserAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'email',
        'username',
        'password',
        'created_at',
        'updated_at'
    )

admin.site.register(User, UserAdmin)
