from django.contrib import admin
from .models import Profile , Address , Favorite , FavoriteProduct

# Create your modeladmin here.

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user' , 'phone_number' , 'natural_id']



@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ['profile' , 'state' , 'city' , 'postal_code']



@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ['user']



@admin.register(FavoriteProduct)
class FavoriteProductAdmin(admin.ModelAdmin):
    list_display = ['favorite' , 'product']