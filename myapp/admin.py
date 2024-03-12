from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'email', 'mobile_number')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    list_display = UserAdmin.list_display + ('mobile_number',)  # Add 'mobile_number' to display

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Categories)
admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(Cart_item)
admin.site.register(Order)
admin.site.register(OrderLine)
admin.site.register(Wishlist)
admin.site.register(BillingAddress)
admin.site.register(ShippingAddress)
