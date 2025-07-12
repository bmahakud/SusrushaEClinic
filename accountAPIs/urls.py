app_name = 'accountAPIs'

from django.urls import path
from .views import (
    UserListView, UserSearchView, RegistrationView, GenerateOTPView, 
    VerifyOTPView, CreateAdminView, CreateDoctorView
)

urlpatterns = [
    # User management
    path('users/', UserListView.as_view(), name='user-list'),
    path('usersearch/', UserSearchView.as_view(), name='user-search'),
    
    # Registration and Authentication
    path('register/', RegistrationView.as_view(), name='register'),
    path('generate-otp/', GenerateOTPView.as_view(), name='generate-otp'),
    path('verify-otp/', VerifyOTPView.as_view(), name='verify-otp'),
    
    # Admin/Doctor Creation (Super Admin only)
    path('create-admin/', CreateAdminView.as_view(), name='create-admin'),
    path('create-doctor/', CreateDoctorView.as_view(), name='create-doctor'),
]




