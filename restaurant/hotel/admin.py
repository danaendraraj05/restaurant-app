from django.contrib import admin
from .models import Cuisine, Restaurant, Photo, Dish, Review

@admin.register(Cuisine)
class CuisineAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('title', 'rating', 'cost_for_two', 'owner', 'location', 'food_type')
    list_filter = ('food_type', 'cuisines')
    search_fields = ('title', 'location', 'owner__username')  # Assuming owner is a ForeignKey to User
    readonly_fields = ('rating',)  # Ensure rating is read-only in admin

    def save_model(self, request, obj, form, change):
        if not obj.owner:
            obj.owner = request.user  # Assign current user as owner if not already set
        super().save_model(request, obj, form, change)

@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ('restaurant', 'image')

@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'dish_type', 'restaurant')
    list_filter = ('dish_type', 'restaurant')
    search_fields = ('name',)

