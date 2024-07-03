from django.db import models
from django.contrib.auth import get_user_model
from hotel.models import Restaurant

class Bookmark(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='bookmarks')
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='bookmark_users')

    class Meta:
        unique_together = ('user', 'restaurant')

    def __str__(self):
        return f'{self.user.username} bookmarks {self.restaurant.title}'