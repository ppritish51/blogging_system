from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from .models import CheetahUser

#ToDo: Make all password write only
class UserSerializer(serializers.ModelSerializer):
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

class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    confirm_new_password = serializers.CharField(required=True)

    def validate(self, data):
        if data['new_password'] != data['confirm_new_password']:
            raise serializers.ValidationError("Passwords do not match.")
        validate_password(data['new_password'])
        return data

class ResetPasswordEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        try:
            user = CheetahUser.objects.get(email=value)
        except CheetahUser.DoesNotExist:
            raise serializers.ValidationError("User with this email does not exist.")
        return value

class ResetPasswordConfirmSerializer(serializers.Serializer):
    uidb64 = serializers.CharField()
    token = serializers.CharField()
    new_password = serializers.CharField()
    confirm_new_password = serializers.CharField()

    def validate(self, attrs):
        new_password = attrs.get('new_password')
        confirm_new_password = attrs.get('confirm_new_password')

        if new_password != confirm_new_password:
            raise serializers.ValidationError("Passwords do not match.")

        return attrs