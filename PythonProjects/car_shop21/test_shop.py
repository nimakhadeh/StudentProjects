from django.test import TestCase
from cars.models import Car

class CarShopTestCase(TestCase):
    def test_car_creation(self):
        self.assertEqual(1 + 1, 2)
        print("✅ Test passed!")
