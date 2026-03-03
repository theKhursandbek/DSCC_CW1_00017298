from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['username', 'email', 'first_name', 'last_name', 'age', 'is_staff']
    fieldsets = list(UserAdmin.fieldsets or []) + [
        (None, {'fields': ('age',)}),
    ]
    add_fieldsets = list(UserAdmin.add_fieldsets or []) + [
        (None, {'fields': ('age',)}),
    ]


admin.site.register(CustomUser, CustomUserAdmin)
