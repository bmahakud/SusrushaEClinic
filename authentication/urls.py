from django.urls import path
from . import views

app_name = 'authentication'

urlpatterns = [
    # Health check
    path('health/', views.health_check, name='health_check'),
    
    # Authentication endpoints
    path('send-otp/', views.SendOTPView.as_view(), name='send_otp'),
    path('verify-otp/', views.VerifyOTPView.as_view(), name='verify_otp'),
    path('refresh/', views.CustomTokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    
    # Profile management
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('change-password/', views.ChangePasswordView.as_view(), name='change_password'),
    
    # Session management
    path('sessions/', views.UserSessionsView.as_view(), name='user_sessions'),
    
    # Admin user management (Admin/SuperAdmin only)
    path('admin/users/', views.AdminUserManagementView.as_view(), name='admin_users'),
    path('admin/users/<str:user_id>/', views.AdminUserDetailView.as_view(), name='admin_user_detail'),
]

