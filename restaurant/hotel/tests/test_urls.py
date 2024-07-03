from django.test import SimpleTestCase
from django.urls import reverse, resolve
from hotel.views import BookmarkToggleView, RestaurantDetailView  # Adjust as per your views

class UrlsTest(SimpleTestCase):
    def test_bookmark_toggle_url(self):
        url = reverse('bookmark_toggle', args=[1])
        self.assertEqual(resolve(url).func.view_class, BookmarkToggleView)

    def test_restaurant_detail_url(self):
        url = reverse('restaurant_detail', args=[1])
        self.assertEqual(resolve(url).func.view_class, RestaurantDetailView)
