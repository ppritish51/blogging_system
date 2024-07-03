from django.urls import path
from .views import PasswordChangeView
from .views import ResetPasswordEmailView
from .views import ResetPasswordConfirmView
from .customAuthToken.views import CustomTokenObtainPairView, CustomTokenRefreshView, CustomRegisterUserView

urlpatterns = [
    # path('register/', CustomRegisterUserView.as_view(), name='register'),
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
    path('change-password/', PasswordChangeView.as_view(), name='change_password'),
    path('reset_password_email/', ResetPasswordEmailView.as_view(), name='reset_password_email'),
    path('reset_password_confirm/', ResetPasswordConfirmView.as_view(), name='reset_password_confirm'),
]
