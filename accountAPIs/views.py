from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
import random
import requests
from django.core.mail import send_mail
from rest_framework_simplejwt.tokens import RefreshToken
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.db.models import Q
from django.shortcuts import get_object_or_404

from .serializers import (
    UserSerializer, UserSearchSerializer, RegistrationSerializer,
    OTPGenerationSerializer, OTPVerificationSerializer, LoginResponseSerializer,
    CreateAdminSerializer, CreateDoctorSerializer, ProfileUpdateSerializer,
    ProfilePhotoUploadSerializer, UserListSerializer, PatientSearchSerializer,
    DoctorSearchSerializer, AdminSearchSerializer
)
from account.models import Account, UserType

User = get_user_model()

class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

class UserSearchView(generics.ListAPIView):
    serializer_class = UserSearchSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        query = self.request.query_params.get('q', None)
        if query:
            return User.objects.filter(username__icontains=query)
        return User.objects.all()

# Profile Management Views
class GetMyProfileView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """Get current user's profile"""
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

class UpdateMyProfileView(APIView):
    permission_classes = [IsAuthenticated]
    
    def put(self, request):
        """Update current user's profile"""
        serializer = ProfileUpdateSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'Profile updated successfully',
                'profile': UserSerializer(request.user).data
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UploadProfilePhotoView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        """Upload profile picture"""
        serializer = ProfilePhotoUploadSerializer(request.user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'Profile photo uploaded successfully',
                'profile_image': request.user.profile_image.url if request.user.profile_image else None
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# User Listing Views with Pagination and Filtering
class ListPatientsView(generics.ListAPIView):
    serializer_class = UserListSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['is_active', 'city', 'state', 'country']
    search_fields = ['firstname', 'lastname', 'email', 'username', 'phoneno']
    ordering_fields = ['firstname', 'lastname', 'date_joined']
    ordering = ['-date_joined']
    
    def get_queryset(self):
        """Get all patients with pagination/filtering"""
        try:
            patient_type = UserType.objects.get(name='patient')
            return User.objects.filter(usertype=patient_type)
        except UserType.DoesNotExist:
            return User.objects.none()

class ListDoctorsView(generics.ListAPIView):
    serializer_class = UserListSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['is_active', 'city', 'state', 'country']
    search_fields = ['firstname', 'lastname', 'email', 'username', 'phoneno']
    ordering_fields = ['firstname', 'lastname', 'date_joined']
    ordering = ['-date_joined']
    
    def get_queryset(self):
        """Get all doctors with pagination/filtering"""
        try:
            doctor_type = UserType.objects.get(name='doctor')
            return User.objects.filter(usertype=doctor_type)
        except UserType.DoesNotExist:
            return User.objects.none()

class ListAdminsView(generics.ListAPIView):
    serializer_class = UserListSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['is_active', 'city', 'state', 'country']
    search_fields = ['firstname', 'lastname', 'email', 'username', 'phoneno']
    ordering_fields = ['firstname', 'lastname', 'date_joined']
    ordering = ['-date_joined']
    
    def get_queryset(self):
        """Get all admins with pagination/filtering"""
        try:
            admin_type = UserType.objects.get(name='clinic_admin')
            return User.objects.filter(usertype=admin_type)
        except UserType.DoesNotExist:
            return User.objects.none()

# Search Views
class SearchPatientsView(generics.ListAPIView):
    serializer_class = PatientSearchSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['is_active', 'city', 'state', 'country']
    search_fields = ['firstname', 'lastname', 'email', 'username', 'phoneno', 'patient_profile__patient_id']
    ordering_fields = ['firstname', 'lastname', 'date_joined']
    ordering = ['-date_joined']
    
    def get_queryset(self):
        """Search patients with advanced filtering"""
        try:
            patient_type = UserType.objects.get(name='patient')
            queryset = User.objects.filter(usertype=patient_type)
            
            # Additional filters
            clinic_center = self.request.query_params.get('clinic_center', None)
            if clinic_center:
                queryset = queryset.filter(patient_profile__clinic_center_id=clinic_center)
            
            return queryset
        except UserType.DoesNotExist:
            return User.objects.none()

class SearchDoctorsView(generics.ListAPIView):
    serializer_class = DoctorSearchSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['is_active', 'city', 'state', 'country']
    search_fields = ['firstname', 'lastname', 'email', 'username', 'phoneno', 'doctor_profile__license_number']
    ordering_fields = ['firstname', 'lastname', 'date_joined']
    ordering = ['-date_joined']
    
    def get_queryset(self):
        """Search doctors with advanced filtering"""
        try:
            doctor_type = UserType.objects.get(name='doctor')
            queryset = User.objects.filter(usertype=doctor_type)
            
            # Additional filters
            clinic_center = self.request.query_params.get('clinic_center', None)
            specialization = self.request.query_params.get('specialization', None)
            
            if clinic_center:
                queryset = queryset.filter(doctor_profile__clinic_center_id=clinic_center)
            
            if specialization:
                queryset = queryset.filter(doctor_profile__specializations__name__icontains=specialization)
            
            return queryset
        except UserType.DoesNotExist:
            return User.objects.none()

class SearchAdminsView(generics.ListAPIView):
    serializer_class = AdminSearchSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['is_active', 'city', 'state', 'country']
    search_fields = ['firstname', 'lastname', 'email', 'username', 'phoneno']
    ordering_fields = ['firstname', 'lastname', 'date_joined']
    ordering = ['-date_joined']
    
    def get_queryset(self):
        """Search admins with advanced filtering"""
        try:
            admin_type = UserType.objects.get(name='clinic_admin')
            queryset = User.objects.filter(usertype=admin_type)
            
            # Additional filters
            clinic_center = self.request.query_params.get('clinic_center', None)
            role = self.request.query_params.get('role', None)
            
            if clinic_center:
                queryset = queryset.filter(admin_profile__clinic_center_id=clinic_center)
            
            if role:
                queryset = queryset.filter(admin_profile__role__icontains=role)
            
            return queryset
        except UserType.DoesNotExist:
            return User.objects.none()



# Registration and OTP Views
class RegistrationView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                'message': 'Account created successfully. Please login with OTP.',
                'user_id': user.id
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GenerateOTPView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = OTPGenerationSerializer(data=request.data)
        if serializer.is_valid():
            phoneno = serializer.validated_data['phoneno']
            try:
                user = User.objects.get(phoneno=phoneno)
                
                # Generate OTP
                otp = str(random.randint(100000, 999999))
                user.temp_otp = otp
                user.otp_created_at = timezone.now()
                user.save()
                
                # Send OTP via SMS (you can customize this)
                self.send_otp_sms(phoneno, otp)
                
                return Response({
                    'message': 'OTP sent successfully to your phone number.',
                    'phoneno': phoneno
                }, status=status.HTTP_200_OK)
                
            except User.DoesNotExist:
                return Response({
                    'error': 'User not found with this phone number.'
                }, status=status.HTTP_404_NOT_FOUND)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def send_otp_sms(self, phoneno, otp):
        """Send OTP via SMS - customize this based on your SMS provider"""
        try:
            # Example using Fast2SMS (you can change this to your preferred provider)
            url = "https://www.fast2sms.com/dev/bulkV2"
            payload = f"variables_values={otp}&route=otp&numbers={phoneno}"
            headers = {
                'authorization': "YOUR_FAST2SMS_API_KEY",  # Replace with your API key
                'Content-Type': "application/x-www-form-urlencoded",
                'Cache-Control': "no-cache",
            }
            response = requests.request("POST", url, data=payload, headers=headers)
            print(f"OTP {otp} sent to {phoneno}")
        except Exception as e:
            print(f"Error sending SMS: {e}")

class VerifyOTPView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = OTPVerificationSerializer(data=request.data)
        if serializer.is_valid():
            phoneno = serializer.validated_data['phoneno']
            otp = serializer.validated_data['otp']
            
            try:
                user = User.objects.get(phoneno=phoneno)
                
                # Check if OTP is valid and not expired (15 minutes)
                if (user.temp_otp == otp and 
                    user.otp_created_at and 
                    timezone.now() - user.otp_created_at < timedelta(minutes=15)):
                    
                    # Clear OTP after successful verification
                    user.temp_otp = None
                    user.otp_created_at = None
                    user.save()
                    
                    # Generate JWT tokens
                    refresh = RefreshToken.for_user(user)
                    
                    # Serialize user data
                    user_serializer = UserSerializer(user)
                    
                    return Response({
                        'access': str(refresh.access_token),
                        'refresh': str(refresh),
                        'user': user_serializer.data,
                        'message': 'Login successful'
                    }, status=status.HTTP_200_OK)
                else:
                    return Response({
                        'error': 'Invalid or expired OTP'
                    }, status=status.HTTP_400_BAD_REQUEST)
                    
            except User.DoesNotExist:
                return Response({
                    'error': 'User not found'
                }, status=status.HTTP_404_NOT_FOUND)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Admin/Doctor Creation Views (Super Admin only)
class CreateAdminView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        # Check if user is super admin
        if not request.user.is_super_admin():
            return Response({
                'error': 'Only super admin can create clinic admins'
            }, status=status.HTTP_403_FORBIDDEN)
        
        serializer = CreateAdminSerializer(data=request.data)
        if serializer.is_valid():
            admin = serializer.save()
            return Response({
                'message': 'Clinic admin created successfully',
                'admin_id': admin.id
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CreateDoctorView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        # Check if user is super admin
        if not request.user.is_super_admin():
            return Response({
                'error': 'Only super admin can create doctors'
            }, status=status.HTTP_403_FORBIDDEN)
        
        serializer = CreateDoctorSerializer(data=request.data)
        if serializer.is_valid():
            doctor = serializer.save()
            return Response({
                'message': 'Doctor created successfully',
                'doctor_id': doctor.id
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




