from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Role

class CustomUserAdmin(UserAdmin):
  
    model = User
    list_display = ['username', 'email', 'role', 'is_staff']
    
   
    fieldsets = UserAdmin.fieldsets + (
        ('Extra Info', {'fields': ('role', 'phone_number', 'address', 'profile_picture')}),
    )

admin.site.register(User, CustomUserAdmin)
admin.site.register(Role)