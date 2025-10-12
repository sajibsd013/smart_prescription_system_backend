
from django.contrib.auth import get_user_model
from rest_framework import generics, status
from .serializers import RegisterSerializer, LoginSerializer, UserSerializer, UserManagementSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.cache import cache
from .healper import sent_email_to_user, verify_otp, sent_otp
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework_simplejwt.tokens import AccessToken
import datetime
User = get_user_model()

# Create your views here.
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

class VerifyEmailView(APIView):
    def post(self, request):
        email = request.data.get("email")
        otp = request.data.get("otp")

        if not email or not otp:
            return Response({"message": "email and otp are required"}, status=status.HTTP_400_BAD_REQUEST)

        # Verify the OTP
        if not verify_otp(email, otp):
            return Response({"message": "Invalid or expired OTP"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email=email)
            user.is_active = True
            user.save()
            cache.delete(f"email_verify_{email}")

            # Create a temporary JWT token (valid for 15 min)
            token = AccessToken.for_user(user)
            token['purpose'] = 'email_verification'
            token.set_exp(
                from_time=datetime.datetime.now(datetime.timezone.utc),
                lifetime=datetime.timedelta(minutes=15)
            )

            sent_email_to_user(user, "Your email has been verified successfully.",
                               "Your email has been verified successfully.")

            return Response(
                {
                    "message": "Email verified successfully",
                    "token": str(token),
                },
                status=status.HTTP_200_OK
            )
        except User.DoesNotExist:
            return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)

class SendAPIView(APIView):
    def post(self, request):
        email = request.data.get("email")
        purpose = request.data.get("purpose")
        if not email:
            return Response({"message": "Email is required"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.get(email=email)
            sent_otp(user.email, purpose)
            return Response({"message": "Verification OTP resent"}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)

class LoginView(TokenObtainPairView):
    serializer_class = LoginSerializer

class LogoutView(APIView):
    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")
            if not refresh_token:
                return Response({"message": "Refresh token is required"}, status=status.HTTP_400_BAD_REQUEST)

            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response({"message": "Logged out successfully"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class UserView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def perform_update(self, serializer):
        serializer.save()

    def perform_destroy(self, instance):
        instance.delete()

class PasswordChangeView(generics.UpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        user = self.get_object()
        old_password = request.data.get("old_password")
        new_password = request.data.get("new_password")
        confirm_password = request.data.get("confirm_password")
        if not old_password or not new_password or not confirm_password:
            return Response({"message": "old_password, new_password and confirm_password are required"}, status=status.HTTP_400_BAD_REQUEST)
        if not user.check_password(old_password):
            return Response({"message": "Old password is incorrect"}, status=status.HTTP_400_BAD_REQUEST)
        if new_password == old_password:
            return Response({"message": "New password cannot be the same as the old password"}, status=status.HTTP_400_BAD_REQUEST)
        if new_password != confirm_password:
            return Response({"message": "New password and confirm password do not match"}, status=status.HTTP_400_BAD_REQUEST)
        user.set_password(new_password)
        user.save()
        return Response({"message": "Password changed successfully"}, status=status.HTTP_200_OK)


class PasswordResetConfirmView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        new_password = request.data.get("new_password")
        confirm_password = request.data.get("confirm_password")

        if new_password != confirm_password:
            return Response({"message": "New password and confirm password do not match"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = request.user
            user.set_password(new_password)
            user.save()

            return Response({"message": "Password reset successfully"}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)



class UserListView(APIView):
    permission_classes = [IsAdminUser]
    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserManagementView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request, user_id):
        try:
            user = User.objects.get(pk=user_id)
            serializer = UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    def patch(self, request, user_id):
        user = User.objects.get(pk=user_id)
        serializer = UserManagementSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, user_id):
      try:
          user = User.objects.get(pk=user_id)
          user.delete()
          return Response(status=status.HTTP_204_NO_CONTENT)
      except User.DoesNotExist:
          return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)



