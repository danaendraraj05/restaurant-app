from django.contrib import admin
from .models import Cuisine, Restaurant, Photo, Dish

@admin.register(Cuisine)
class CuisineAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('title', 'rating', 'cost_for_two', 'owner', 'location', 'food_type')
    list_filter = ('food_type', 'cuisines')
    search_fields = ('title', 'location', 'owner')

@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ('restaurant', 'image')

@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'dish_type', 'restaurant')
    list_filter = ('dish_type', 'restaurant')
    search_fields = ('name',)

