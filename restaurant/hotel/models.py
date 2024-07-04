from django.db import models
from django.contrib.auth.models import User
from django.db.models import Avg

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
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.0)
    cost_for_two = models.DecimalField(max_digits=6, decimal_places=2)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, editable=False)
    location = models.CharField(max_length=255)
    address = models.TextField()
    opening_time = models.TimeField()
    closing_time = models.TimeField()
    food_type = models.CharField(max_length=7, choices=FOOD_TYPE_CHOICES)
    cuisines = models.ManyToManyField(Cuisine, related_name='restaurants')
    
    def bookmarked_users(self):
        return self.bookmark_users.all().values_list('username', flat=True)

    def visited_users(self):
        return self.visited_users.all().values_list('username', flat=True)

    @property
    def average_rating(self):
        reviews = self.reviews.all()
        if reviews:
            return reviews.aggregate(Avg('rating'))['rating__avg']
        return 0.0

    def save(self, *args, **kwargs):
        if not self.id:  # If creating a new instance
            self.owner = User.objects.filter(is_staff=True, is_superuser=True).first()  # Assign the first admin user
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Photo(models.Model):
    restaurant = models.ForeignKey(Restaurant, related_name='photos', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='static/restaurant_photos/')

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

class Review(models.Model):
    restaurant = models.ForeignKey(Restaurant, related_name='reviews', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField()
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Review by {self.user} for {self.restaurant}"
