from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView
from .serializers import CustomTokenObtainPairSerializer, CustomTokenRefreshSerializer, RegisterUserSerializer
from ..models import CheetahUser
from rest_framework.permissions import AllowAny
from rest_framework.throttling import AnonRateThrottle


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class CustomTokenRefreshView(TokenRefreshView):
    serializer_class = CustomTokenRefreshSerializer


class CustomRegisterUserView(generics.CreateAPIView):
    queryset = CheetahUser.objects.all()
    serializer_class = RegisterUserSerializer
    permission_classes = (AllowAny,)
    throttle_classes = (AnonRateThrottle,)
    
    def create(self, request, *args, **kwargs):
        response = super(CustomRegisterUserView, self).create(request, *args, **kwargs)
        
        # Check if user is created successfully
        if response.status_code == status.HTTP_201_CREATED:
            user = CheetahUser.objects.get(email=response.data['email'])
            tokens = RegisterUserSerializer().get_tokens_for_user(user)

            # Extract credit_left and is_resume_uploaded attributes.
            # This is just an example. Adjust this according to your model structure.
            credit_left = user.interrogabot_v2_credits.credit_left if hasattr(user, 'credits') else 10
            is_resume_uploaded = user.original_resume.is_original if hasattr(user, 'original_resume') else False
            resume_filename = user.original_resume.filename if hasattr(user, 'original_resume') else ""

            return Response({
                'refresh': tokens['refresh'],
                'access': tokens['access'],
                'user': {
                    'email': response.data['email'],
                    'name': response.data['name'],
                    'mobile': response.data['mobile_number_with_country_code'], 
                    'credit_left': credit_left,
                    'is_resume_uploaded': is_resume_uploaded,
                    'resume_filename': resume_filename
                }
            }, status=status.HTTP_201_CREATED)

        return response
