from django.test import TestCase
from hotel.forms import ReviewForm

class ReviewFormTests(TestCase):
    def test_valid_form(self):
        data = {
            'text': 'Great place!',
            'rating': 5
        }
        form = ReviewForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        data = {
            'text': '',
            'rating': 5
        }
        form = ReviewForm(data=data)
        self.assertFalse(form.is_valid())
