from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView
)
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register('doctor', DoctorViewSet)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('verify/', VerifyEmailView.as_view(), name='verify-email'),
    path('send-otp/', SendAPIView.as_view(), name='send-otp'),
    path('login/', LoginView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('user/', UserView.as_view(), name='user-details'),
    path('change-password/', PasswordChangeView.as_view(), name='change-password'),
    path('reset-password/', PasswordResetConfirmView.as_view(), name='reset-password-confirm'),
    path('users/', UserListView.as_view(), name='user-list'),
    path('users/<int:user_id>/', UserManagementView.as_view(), name='user-management'),
    path('', include(router.urls)),

]
