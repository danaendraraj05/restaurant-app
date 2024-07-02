from django.db import models

class Cuisine(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Restaurant(models.Model):
    VEG = 'Veg'
    NON_VEG = 'Non-Veg'
    VEGAN = 'Vegan'
    FOOD_TYPE_CHOICES = [
        (VEG, 'Vegetarian'),
        (NON_VEG, 'Non-Vegetarian'),
        (VEGAN, 'Vegan'),
    ]

    title = models.CharField(max_length=255)
    rating = models.DecimalField(max_digits=3, decimal_places=2)
    reviews = models.TextField()
    cost_for_two = models.DecimalField(max_digits=6, decimal_places=2)
    owner = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    address = models.TextField()
    timings = models.CharField(max_length=100)
    food_type = models.CharField(max_length=7, choices=FOOD_TYPE_CHOICES)
    cuisines = models.ManyToManyField(Cuisine, related_name='restaurants')

    def __str__(self):
        return self.title

class Photo(models.Model):
    restaurant = models.ForeignKey(Restaurant, related_name='photos', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='restaurant_photos/')

    def __str__(self):
        return f"Photo for {self.restaurant.title}"

class Dish(models.Model):
    VEG = 'Veg'
    NON_VEG = 'Non-Veg'
    DISH_TYPE_CHOICES = [
        (VEG, 'Vegetarian'),
        (NON_VEG, 'Non-Vegetarian'),
    ]

    restaurant = models.ForeignKey(Restaurant, related_name='dishes', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    dish_type = models.CharField(max_length=7, choices=DISH_TYPE_CHOICES)

    def __str__(self):
        return f"{self.name} ({self.dish_type}) - {self.restaurant.title}"
