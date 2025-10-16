from rest_framework import serializers
from django.contrib.auth import get_user_model
from .healper import sent_otp
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.models import update_last_login
from .models import Doctor, Patient

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ( 'email', 'name', 'phone', 'password', 'confirm_password')

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
        fields = ['id', 'email', 'name',  'phone', 'is_active', 'is_staff', 'is_superuser', 'is_verified','last_login','created_at']
        read_only_fields = ['id', 'email', 'is_active', 'is_staff', 'is_superuser', 'is_verified','last_login','created_at']


class UserManagementSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'name',  'phone', 'is_active', 'is_staff', 'is_superuser', 'is_verified','last_login','created_at']
        read_only_fields = ['id', 'email', 'is_superuser','last_login','created_at']



class DoctorSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Doctor
        fields = '__all__'
        read_only_fields = ['id', 'user', 'created_at','modified_at']

    def validate_user(self, value):
        """
        Ensure a user cannot be assigned to more than one Doctor.
        """
        qs = Doctor.objects.filter(user=value)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError("This user already has a doctor profile.")
        return value

    def create(self, validated_data):
        user = validated_data.get('user')
        if Doctor.objects.filter(user=user).exists():
            raise serializers.ValidationError({"user": "This user already has a doctor profile."})
        return super().create(validated_data)

class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = '__all__'
