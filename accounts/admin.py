from django.contrib import admin

from .models import Profile, Address


@admin.register(Profile)
class Profile(admin.ModelAdmin):
    list_display = ['user', 'mobile']
    search_fields = ['user', 'mobile']
    list_filter = ['user', 'mobile']
    list_per_page = 10


@admin.register(Address)
class Address(admin.ModelAdmin):
    list_display = ['profile', 'type', 'city', 'country', 'pincode']
    search_fields = ['profile', 'type', 'city', 'country', 'pincode']
    list_filter = ['profile', 'type', 'city', 'country', 'pincode']
    list_per_page = 10
