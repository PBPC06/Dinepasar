from django.test import TestCase
from .models import Review

# Dinepasar/review/test_tests.py


class ReviewModelTest(TestCase):

    def setUp(self):
        # Set up a sample review object
        self.review = Review.objects.create(
            title="Great Restaurant",
            content="The food was amazing and the service was excellent.",
            rating=5
        )

    def test_review_creation(self):
        # Test if the review object is created correctly
        self.assertEqual(self.review.title, "Great Restaurant")
        self.assertEqual(self.review.content, "The food was amazing and the service was excellent.")
        self.assertEqual(self.review.rating, 5)

    def test_review_str_method(self):
        # Test the __str__ method of the Review model
        self.assertEqual(str(self.review), "Great Restaurant")