from django.contrib import admin
from .models import User


# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    model = User
    list_display = ['email', 'full_name', 'is_active', 'is_teacher']
    list_filter = ['is_active', 'date_joined', 'is_teacher']
    search_fields = ['email', 'full_name']
