app_name = 'accountAPIs'

from django.urls import path
from .views import (
    UserListView, UserSearchView, RegistrationView, GenerateOTPView, 
    VerifyOTPView, CreateAdminView, CreateDoctorView, GetMyProfileView,
    UpdateMyProfileView, UploadProfilePhotoView, ListPatientsView,
    ListDoctorsView, ListAdminsView, SearchPatientsView, SearchDoctorsView,
    SearchAdminsView
)

urlpatterns = [
    # User management
    path('users/', UserListView.as_view(), name='user-list'),
    path('usersearch/', UserSearchView.as_view(), name='user-search'),
    
    # Profile Management
    path('profile/', GetMyProfileView.as_view(), name='get-profile'),
    path('profile/update/', UpdateMyProfileView.as_view(), name='update-profile'),
    path('profile/upload-photo/', UploadProfilePhotoView.as_view(), name='upload-photo'),
    
    # User Listing by Type
    path('patients/', ListPatientsView.as_view(), name='list-patients'),
    path('doctors/', ListDoctorsView.as_view(), name='list-doctors'),
    path('admins/', ListAdminsView.as_view(), name='list-admins'),
    
    # Search Endpoints
    path('search/patients/', SearchPatientsView.as_view(), name='search-patients'),
    path('search/doctors/', SearchDoctorsView.as_view(), name='search-doctors'),
    path('search/admins/', SearchAdminsView.as_view(), name='search-admins'),
    

    
    # Registration and Authentication
    path('register/', RegistrationView.as_view(), name='register'),
    path('generate-otp/', GenerateOTPView.as_view(), name='generate-otp'),
    path('verify-otp/', VerifyOTPView.as_view(), name='verify-otp'),
    
    # Admin/Doctor Creation (Super Admin only)
    path('create-admin/', CreateAdminView.as_view(), name='create-admin'),
    path('create-doctor/', CreateDoctorView.as_view(), name='create-doctor'),
]




