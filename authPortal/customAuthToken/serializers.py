from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from ..models import CheetahUser

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        
        # Add custom claims
        token['email'] = user.email
        token['name'] = user.name
        # Add more claims as required
        
        return token

    def validate(self, attrs):
        data = super().validate(attrs)

        # Try to retrieve the UserCredit object for the authenticated user
        user_credit = self.user.interrogabot_v2_credits.credit_left if hasattr(self.user, 'credits') else 0
        user_resume = self.user.original_resume.is_original if hasattr(self.user, 'original_resume') else False
        resume_filename = self.user.original_resume.filename if hasattr(self.user, 'original_resume') else ""
        
        # Add user details to the response
        data.update({
            'user': {
                'email': self.user.email,
                'name': self.user.name,
                'mobile': self.user.mobile_number_with_country_code,
                'credit_left': user_credit, 
                'is_resume_uploaded': user_resume,
                'resume_filename': resume_filename
                # Add more details as required
            }
        })

        return data

class CustomTokenRefreshSerializer(TokenRefreshSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        # Retrieve the existing refresh token from the request
        existing_refresh_token = attrs['refresh']

        # Decode the token and retrieve the user
        refresh = RefreshToken(existing_refresh_token)
        
        # Assuming the user's ID is in the token. Adjust if needed.
        user_id = refresh['user_id']
        user = CheetahUser.objects.get(id=user_id)
        
        # Continue with your original code
        user_credit = user.interrogabot_v2_credits.credit_left if hasattr(user, 'credits') else 0
        user_resume = user.original_resume.is_original if hasattr(user, 'original_resume') else False
        resume_filename = user.original_resume.filename if hasattr(user, 'original_resume') else ""

        data.update({
            'refresh': existing_refresh_token,  # Add the existing refresh token back to the response
            'user': {
                'email': user.email,
                'name': user.name,
                'mobile': user.mobile_number_with_country_code,
                'credit_left': user_credit, 
                'is_resume_uploaded': user_resume,
                'resume_filename': resume_filename
            }
        })

        return data

#ToDo: Make all password write only
class RegisterUserSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = CheetahUser
        fields = ('email', 'name', 'mobile_number_with_country_code', 'password', 'confirm_password')
        extra_kwargs = {
            'password': {'write_only': True},
            'confirm_password': {'write_only': True}
        }

    def validate(self, attrs):
        password = attrs.get('password')
        confirm_password = attrs.get('confirm_password')

        if password != confirm_password:
            raise serializers.ValidationError({"confirm_password": "Passwords do not match"})

        return attrs

    def validate_password(self, value):
        validate_password(value)
        return value

    def create(self, validated_data):
        confirm_password = validated_data.pop('confirm_password')
        user = CheetahUser.objects.create_user(**validated_data)
        return user
    
    def get_tokens_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
