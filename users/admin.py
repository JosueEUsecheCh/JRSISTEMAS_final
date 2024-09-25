from django.contrib import admin
from .models import User_register

@admin.register(User_register)
class UserRegisterAdmin(admin.ModelAdmin):
    list_display = ('name', 'last_name', 'email', 'phone_number', 'is_staff', 'is_superuser')
    search_fields = ('email', 'name', 'last_name')
    list_filter = ('is_staff', 'is_superuser')


