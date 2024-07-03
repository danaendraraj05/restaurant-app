from django.test import TestCase
from django.contrib.auth import get_user_model
from hotel.models import Restaurant, Dish, Photo, Review

User = get_user_model()

class RestaurantModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.restaurant = Restaurant.objects.create(
            title='Test Restaurant',
            cost_for_two=500,
            owner=self.user,
            location='Test Location',
            address='Test Address',
            opening_time='10:00:00',
            closing_time='22:00:00',
            food_type='Test Food'
        )

    def test_restaurant_creation(self):
        self.assertEqual(self.restaurant.title, 'Test Restaurant')
        self.assertEqual(self.restaurant.cost_for_two, 500)
        self.assertEqual(self.restaurant.owner, self.user)

    def test_add_dish(self):
        dish = Dish.objects.create(
            name='Test Dish',
            price=100,
            dish_type='Main Course',
            restaurant=self.restaurant
        )
        self.assertEqual(dish.name, 'Test Dish')
        self.assertEqual(dish.price, 100)

    def test_add_photo(self):
        photo = Photo.objects.create(
            restaurant=self.restaurant,
            image='test_image.jpg'
        )
        self.assertEqual(photo.restaurant, self.restaurant)

    def test_add_review(self):
        review = Review.objects.create(
            restaurant=self.restaurant,
            user=self.user,
            text='Great place!',
            rating=5
        )
        self.assertEqual(review.restaurant, self.restaurant)
        self.assertEqual(review.user, self.user)
        self.assertEqual(review.text, 'Great place!')
        self.assertEqual(review.rating, 5)
