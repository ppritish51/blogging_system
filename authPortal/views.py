from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle
from rest_framework.permissions import AllowAny, IsAuthenticated

from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings

from email_service.email_utils import send_forgot_password_email
from rest_framework.throttling import ScopedRateThrottle

from .serializers import UserSerializer, PasswordChangeSerializer
from .serializers import ResetPasswordEmailSerializer
from .serializers import ResetPasswordConfirmSerializer

from .models import CheetahUser
from django.contrib.auth import get_user_model


class RegisterUserView(generics.CreateAPIView):
    queryset = CheetahUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)
    throttle_classes = (AnonRateThrottle,)

class PasswordChangeView(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = PasswordChangeSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = request.user
        if not user.check_password(serializer.validated_data['old_password']):
            return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(serializer.validated_data['new_password'])
        user.save()
        return Response({"detail": "Password changed successfully"}, status=status.HTTP_200_OK)

class ResetPasswordEmailView(generics.GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = ResetPasswordEmailSerializer
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'password_reset_via_email'

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        email = serializer.validated_data["email"]
        user = CheetahUser.objects.get(email=email)

        # Generate reset_password_link
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        base_url = settings.RESET_PASSWORD_BASE_URL
        reset_password_link = f"{base_url}?uidb64={uid}&token={token}"

        # Send the forgot password email
        send_forgot_password_email(user.email, email, reset_password_link)

        return Response({"detail": "Reset password link has been sent to the email."},
                        status=status.HTTP_200_OK)

class ResetPasswordConfirmView(generics.GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = ResetPasswordConfirmSerializer
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'password_reset_via_email'

    def post(self, request, *args, **kwargs):
        User = get_user_model()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        uidb64 = serializer.validated_data['uidb64']
        token = serializer.validated_data['token']
        new_password = serializer.validated_data['new_password']

        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            user.set_password(new_password)
            user.save()
            return Response({"success": "Password reset successful."}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid token."}, status=status.HTTP_400_BAD_REQUEST)


