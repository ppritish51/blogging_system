from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

CheetahUser = get_user_model()

class TestAuthViews(APITestCase):

    def test_registration(self):
        data = {
            "email": "testuser@example.com",
            "name": "Test User",
            "mobile_number_with_country_code": "+1234567890",
            "password": "P@$$word123",
            "confirm_password": "P@$$word123",
        }
        url = reverse('register')
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_registration_password_mismatch(self):
        data = {
            "email": "testuser@example.com",
            "name": "Test User",
            "mobile_number_with_country_code": "+1234567890",
            "password": "password123",
            "confirm_password": "password321",
        }
        url = reverse('register')
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_weak_password_registration(self):
        url = reverse('register')
        data = {
            "email": "testuser@example.com",
            "name": "Test User",
            "mobile_number_with_country_code": "+1234567890",
            "password": "password123",
            "confirm_password": "password123",
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('password', response.data)

    def test_registration_email_already_taken(self):
        existing_user_data = {
            "email": "testuser@example.com",
            "name": "Test User",
            "mobile_number_with_country_code": "+1234567890",
            "password": "P@$$word123",
            "confirm_password": "P@$$word123",
        }
        url = reverse('register')
        self.client.post(url, existing_user_data, format='json')

        new_user_data = {
            "email": "testuser@example.com",
            "name": "New Test User",
            "mobile_number_with_country_code": "+1234567891",
            "password": "P@$$word456",
            "confirm_password": "P@$$word456",
        }
        response = self.client.post(url, new_user_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)

    def test_registration_mobile_already_taken(self):
        existing_user_data = {
            "email": "testuser@example.com",
            "name": "Test User",
            "mobile_number_with_country_code": "+1234567890",
            "password": "P@$$word123",
            "confirm_password": "P@$$word123",
        }
        url = reverse('register')
        self.client.post(url, existing_user_data, format='json')

        new_user_data = {
            "email": "newtestuser@example.com",
            "name": "New Test User",
            "mobile_number_with_country_code": "+1234567890",
            "password": "P@$$word456",
            "confirm_password": "P@$$word456",
        }
        response = self.client.post(url, new_user_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('mobile_number_with_country_code', response.data)


class TestPasswordChangeView(APITestCase):
    def setUp(self):
        self.user = CheetahUser.objects.create_user(
            email='testuser@example.com',
            password='P@$$word123',
            mobile_number_with_country_code='+1234567890'
        )
        self.url = reverse('change_password')

    def test_password_change(self):
        self.client.force_authenticate(user=self.user)
        data = {
            'old_password': 'P@$$word123',
            'new_password': 'N3wP@$$w0rd',
            'confirm_new_password': 'N3wP@$$w0rd'
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('N3wP@$$w0rd'))

    def test_password_change_wrong_old_password(self):
        self.client.force_authenticate(user=self.user)
        data = {
            'old_password': 'WrongP@$$word',
            'new_password': 'N3wP@$$w0rd',
            'confirm_new_password': 'N3wP@$$w0rd'
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_change_new_password_mismatch(self):
        self.client.force_authenticate(user=self.user)
        data = {
            'old_password': 'P@$$word123',
            'new_password': 'N3wP@$$w0rd',
            'confirm_new_password': 'D!ff3r3ntP@$$w0rd'
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_change_unauthenticated(self):
        data = {
            'old_password': 'P@$$word123',
            'new_password': 'N3wP@$$w0rd',
            'confirm_new_password': 'N3wP@$$w0rd'
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)