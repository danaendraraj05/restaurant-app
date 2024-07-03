# hotel/tests/test_urls.py

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from hotel.models import Restaurant, Cuisine, Review
from accounts.models import Bookmark

class UrlsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='password')
        self.user.set_password('password')
        self.user.save()
        
        self.cuisine = Cuisine.objects.create(name='Italian')
        self.restaurant = Restaurant.objects.create(
            title='Test Restaurant',
            rating=4.5,
            cost_for_two=50.00,
            owner=self.user,
            location='Sample Location',
            address='Sample Address',
            opening_time='08:00:00',
            closing_time='22:00:00',
            food_type=Restaurant.VEG,
        )
        self.restaurant.cuisines.add(self.cuisine)
        
        self.review = Review.objects.create(
            restaurant=self.restaurant,
            user=self.user,
            rating=4,
            text='Great food and service!'
        )

    def test_restaurant_list_url(self):
        response = self.client.get(reverse('restaurant-list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'hotel/restaurant_list.html')

    def test_restaurant_detail_url(self):
        response = self.client.get(reverse('restaurant-detail', args=[self.restaurant.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'hotel/restaurant_detail.html')

    def test_add_review_url(self):
        self.client.login(username='testuser', password='password')
        response = self.client.get(reverse('add-review', args=[self.restaurant.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'hotel/review_form.html')

    def test_edit_review_url(self):
        self.client.login(username='testuser', password='password')
        response = self.client.get(reverse('edit-review', args=[self.review.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'hotel/review_form.html')

    def test_bookmark_toggle_url(self):
        self.client.login(username='testuser', password='password')
        response = self.client.post(reverse('bookmark-toggle', args=[self.restaurant.id]))
        self.assertEqual(response.status_code, 200)  # Assuming it returns a JSON response

    def test_my_bookmarked_restaurants_url(self):
        self.client.login(username='testuser', password='password')

        # Create a bookmark for the restaurant
        Bookmark.objects.create(user=self.user, restaurant=self.restaurant)

        response = self.client.get(reverse('my-bookmarked-restaurants'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'hotel/bookmarked_restaurants.html')
        self.assertContains(response, 'Test Restaurant')  # Check if the restaurant is in the response

    def test_remove_bookmark_url(self):
        self.client.login(username='testuser', password='password')
        bookmark = Bookmark.objects.create(user=self.user, restaurant=self.restaurant)
        response = self.client.post(reverse('remove-bookmark', args=[self.restaurant.id]))
        self.assertEqual(response.status_code, 302)  # Assuming it redirects after removing bookmark
