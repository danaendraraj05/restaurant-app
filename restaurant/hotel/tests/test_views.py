from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from accounts.models import Bookmark  # Adjust the import path as necessary
from hotel.models import Restaurant

class BookmarkToggleViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.restaurant = Restaurant.objects.create(title='Test Restaurant', owner=self.user)

    def test_bookmark_toggle(self):
        self.client.force_login(self.user)
        url = reverse('bookmark_toggle', args=[self.restaurant.pk])
        response = self.client.post(url)
        
        # Assert that the bookmark was added successfully
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.user.bookmarks.count(), 1)
        self.assertEqual(self.user.bookmarks.first().restaurant, self.restaurant)

    def test_bookmark_remove(self):
        # Setup: Add bookmark first
        Bookmark.objects.create(user=self.user, restaurant=self.restaurant)

        self.client.force_login(self.user)
        url = reverse('bookmark_toggle', args=[self.restaurant.pk])
        response = self.client.post(url)
        
        # Assert that the bookmark was removed successfully
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.user.bookmarks.count(), 0)
