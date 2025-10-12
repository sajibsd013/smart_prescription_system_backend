from rest_framework import serializers
from django.contrib.auth import get_user_model
from .healper import sent_otp
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.models import update_last_login
User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ( 'email', 'first_name', 'last_name','role', 'phone', 'password', 'confirm_password')

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        confirm_password = validated_data.pop('confirm_password', None)
        if password != confirm_password:
            raise serializers.ValidationError("Passwords do not match.")
        user = User.objects.create_user(**validated_data)
        user.is_active = False
        user.set_password(password)
        user.save()

        # Send OTP for email verification
        sent_otp(user.email, purpose="signup")
        return user


class LoginSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['email'] = user.email
        return token

    def validate(self, attrs):
        attrs['email'] = attrs['email'].lower()

        data = super().validate(attrs)
        data['user'] = UserSerializer(self.user).data
        update_last_login(None, self.user)
        return data


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name','last_name', 'role', 'phone', 'is_active', 'is_staff', 'is_superuser', 'is_verified','last_login','created_at']
        read_only_fields = ['id', 'email', 'is_active', 'is_staff', 'is_superuser', 'is_verified','last_login','created_at']


class UserManagementSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name','last_name', 'role', 'phone', 'is_active', 'is_staff', 'is_superuser', 'is_verified','last_login','created_at']
        read_only_fields = ['id', 'email', 'is_superuser','last_login','created_at']
