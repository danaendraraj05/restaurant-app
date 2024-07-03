from django.test import TestCase
from django.contrib.auth.models import User
from hotel.models import Restaurant, Cuisine, Review

class RestaurantModelTests(TestCase):

    def setUp(self):
        self.user = User.objects.create(username='testuser', password='password', is_staff=True, is_superuser=True)
        self.cuisine1 = Cuisine.objects.create(name='Italian')
        self.cuisine = Cuisine.objects.create(name='Indian')
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

    def test_restaurant_creation(self):
        restaurant = Restaurant.objects.get(id=self.restaurant.id)
        self.assertEqual(restaurant.title, 'Test Restaurant')
        self.assertEqual(restaurant.rating, 4.5)
        self.assertEqual(restaurant.cost_for_two, 50.00)
        self.assertEqual(restaurant.owner, self.user)
        self.assertEqual(restaurant.location, 'Sample Location')
        self.assertEqual(restaurant.address, 'Sample Address')
        self.assertEqual(restaurant.opening_time.strftime('%H:%M:%S'), '08:00:00')
        self.assertEqual(restaurant.closing_time.strftime('%H:%M:%S'), '22:00:00')
        self.assertEqual(restaurant.food_type, Restaurant.VEG)

    def test_average_rating_property(self):
        self.assertEqual(self.restaurant.average_rating, 4.0)  # One review with rating 4, so average rating should be 4.0

    def test_bookmarked_users_method(self):
        self.assertEqual(list(self.restaurant.bookmarked_users()), [])  # No bookmarks initially

    def test_restaurant_str_representation(self):
        restaurant = Restaurant.objects.get(id=self.restaurant.id)
        self.assertEqual(str(restaurant), 'Test Restaurant')

    def test_review_creation(self):
        review = Review.objects.get(id=self.review.id)
        self.assertEqual(review.restaurant, self.restaurant)
        self.assertEqual(review.user, self.user)
        self.assertEqual(review.rating, 4)
        self.assertEqual(review.text, 'Great food and service!')

    def test_review_str_representation(self):
        review = Review.objects.get(id=self.review.id)
        expected_str = f"Review by {self.user} for {self.restaurant}"
        self.assertEqual(str(review), expected_str)

    def test_cuisine_creation(self):
        cuisine = Cuisine.objects.get(id=self.cuisine.id)
        self.assertEqual(cuisine.name, 'Indian')

    def test_cuisine_str_representation(self):
        cuisine = Cuisine.objects.get(id=self.cuisine1.id)
        self.assertEqual(str(cuisine), 'Italian')
