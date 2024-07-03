# from django.urls import reverse
# from django.contrib.auth.tokens import default_token_generator
# from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
# from django.test import TestCase
# from rest_framework.test import APITestCase, APIClient
# from authPortal.models import CheetahUser
# from rest_framework import status

# from django.test import override_settings
# from django.core.mail import send_mail

# class PasswordResetTest(APITestCase):
#     def setUp(self):
#         self.client = APIClient()
#         self.user = CheetahUser.objects.create_user(
#             email='test@example.com',
#             name='Test User',
#             mobile_number_with_country_code='+11234567890',
#             password='test_password'
#         )

#     def test_send_password_reset_email(self):
#         url = reverse('reset_password_email')
#         response = self.client.post(url, {'email': self.user.email})
#         self.assertEqual(response.status_code, status.HTTP_200_OK)

#     @override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend')
#     def test_password_reset(self):
#         url = reverse('reset_password_email')
#         self.client.post(url, {'email': self.user.email})

#         from_email = 'noreply@example.com'
#         recipient_list = [self.user.email]
#         message = send_mail(subject='Reset Your Password',
#                                 message='Please follow the link to reset your password',
#                                 from_email=from_email, recipient_list=recipient_list)
#         self.assertEqual(message, 1)
#         uidb64 = urlsafe_base64_encode(str(self.user.pk).encode())
#         token = default_token_generator.make_token(self.user)
#         new_password = 'new_password'

#         url = reverse('reset_password_confirm')
#         response = self.client.post(url, {
#             'uidb64': uidb64,
#             'token': token,
#             'new_password': new_password,
#             'confirm_password': new_password
#         })
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.user.refresh_from_db()
#         self.assertTrue(self.user.check_password(new_password))
