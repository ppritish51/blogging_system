from rest_framework import serializers
from rest_framework.test import APITestCase
from ..serializers import UserSerializer

class TestUserSerializer(APITestCase):

    def test_password_mismatch(self):
        data = {
            "email": "testuser@example.com",
            "name": "Test User",
            "mobile_number_with_country_code": "+1234567890",
            "password": "P@$$word123",
            "confirm_password": "password321",
        }
        serializer = UserSerializer(data=data)

        self.assertFalse(serializer.is_valid())
        self.assertEqual(
            serializer.errors['confirm_password'],
            ["Passwords do not match"]
        )

    def test_valid_user(self):
        data = {
            "email": "testuser@example.com",
            "name": "Test User",
            "mobile_number_with_country_code": "+1234567890",
            "password": "P@$$word123",
            "confirm_password": "P@$$word123",
        }
        serializer = UserSerializer(data=data)

        self.assertTrue(serializer.is_valid())
