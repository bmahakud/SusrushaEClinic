from rest_framework import serializers
from account.models import Account, UserType
from django.contrib.auth import get_user_model
User = get_user_model()
import random
import requests
from django.core.mail import send_mail
from rest_framework_simplejwt.tokens import RefreshToken
from django.db.models import Q

# Only keep serializers for Account and UserType

class UserSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','firstname', 'lastname','usertype','profile_image')

class ContactSerializer(serializers.ModelSerializer):
     class Meta:
         model = User
         fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','firstname', 'lastname','email','username','phoneno','about','usertype','profile_image','gender','dateofbirth','address','city','state','country']
        depth=1

# Profile Management Serializers
class ProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['firstname', 'lastname', 'email', 'about', 'gender', 'dateofbirth', 'address', 'city', 'state', 'country', 'pincode']
        read_only_fields = ['username', 'phoneno', 'usertype']

class ProfilePhotoUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['profile_image']

class UserListSerializer(serializers.ModelSerializer):
    usertype_name = serializers.CharField(source='usertype.name', read_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'firstname', 'lastname', 'email', 'username', 'phoneno', 'usertype', 'usertype_name', 'profile_image', 'is_active', 'date_joined']

# Search Serializers
class PatientSearchSerializer(serializers.ModelSerializer):
    usertype_name = serializers.CharField(source='usertype.name', read_only=True)
    patient_id = serializers.CharField(source='patient_profile.patient_id', read_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'firstname', 'lastname', 'email', 'username', 'phoneno', 'usertype', 'usertype_name', 'profile_image', 'patient_id', 'is_active', 'date_joined']

class DoctorSearchSerializer(serializers.ModelSerializer):
    usertype_name = serializers.CharField(source='usertype.name', read_only=True)
    license_number = serializers.CharField(source='doctor_profile.license_number', read_only=True)
    specializations = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ['id', 'firstname', 'lastname', 'email', 'username', 'phoneno', 'usertype', 'usertype_name', 'profile_image', 'license_number', 'specializations', 'is_active', 'date_joined']
    
    def get_specializations(self, obj):
        if hasattr(obj, 'doctor_profile'):
            return [spec.name for spec in obj.doctor_profile.specializations.all()]
        return []

class AdminSearchSerializer(serializers.ModelSerializer):
    usertype_name = serializers.CharField(source='usertype.name', read_only=True)
    role = serializers.CharField(source='admin_profile.role', read_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'firstname', 'lastname', 'email', 'username', 'phoneno', 'usertype', 'usertype_name', 'profile_image', 'role', 'is_active', 'date_joined']



# Registration and OTP Serializers
class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['phoneno', 'firstname', 'lastname', 'email']
    
    def create(self, validated_data):
        # Generate a unique username based on phone number
        phoneno = validated_data.get('phoneno')
        username = f"user_{phoneno}"
        
        # Create user with patient user type
        user = User.objects.create(
            username=username,
            phoneno=phoneno,
            firstname=validated_data.get('firstname', ''),
            lastname=validated_data.get('lastname', ''),
            email=validated_data.get('email', ''),
        )
        
        # Set patient user type
        try:
            patient_type = UserType.objects.get(name='patient')
            user.usertype = patient_type
        except UserType.DoesNotExist:
            # Create patient user type if it doesn't exist
            patient_type = UserType.objects.create(name='patient')
            user.usertype = patient_type
        
        user.save()
        return user

class OTPGenerationSerializer(serializers.Serializer):
    phoneno = serializers.CharField(max_length=20)
    
    def validate_phoneno(self, value):
        # Check if user exists
        try:
            user = User.objects.get(phoneno=value)
            return value
        except User.DoesNotExist:
            raise serializers.ValidationError("User with this phone number does not exist.")

class OTPVerificationSerializer(serializers.Serializer):
    phoneno = serializers.CharField(max_length=20)
    otp = serializers.CharField(max_length=6)
    
    def validate(self, attrs):
        phoneno = attrs.get('phoneno')
        otp = attrs.get('otp')
        
        try:
            user = User.objects.get(phoneno=phoneno)
            # Check if OTP matches (you might want to store OTP in user model or cache)
            # For now, we'll use a simple approach
            if hasattr(user, 'temp_otp') and user.temp_otp == otp:
                return attrs
            else:
                raise serializers.ValidationError("Invalid OTP")
        except User.DoesNotExist:
            raise serializers.ValidationError("User not found")
        
        return attrs

class LoginResponseSerializer(serializers.Serializer):
    access = serializers.CharField()
    refresh = serializers.CharField()
    user = UserSerializer()

# Admin/Doctor Creation Serializers
class CreateAdminSerializer(serializers.ModelSerializer):
    clinic_center_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'phoneno', 'firstname', 'lastname', 'clinic_center_id']
    
    def create(self, validated_data):
        clinic_center_id = validated_data.pop('clinic_center_id')
        
        # Create user with admin user type
        user = User.objects.create(**validated_data)
        
        try:
            admin_type = UserType.objects.get(name='clinic_admin')
            user.usertype = admin_type
        except UserType.DoesNotExist:
            admin_type = UserType.objects.create(name='clinic_admin')
            user.usertype = admin_type
        
        user.save()
        
        # Create AdminProfile
        from account.models import EClinicCenter, AdminProfile
        try:
            clinic_center = EClinicCenter.objects.get(id=clinic_center_id)
            AdminProfile.objects.create(
                account=user,
                clinic_center=clinic_center,
                role="Admin"
            )
        except EClinicCenter.DoesNotExist:
            raise serializers.ValidationError("Clinic center not found")
        
        return user

class CreateDoctorSerializer(serializers.ModelSerializer):
    clinic_center_id = serializers.IntegerField(write_only=True)
    license_number = serializers.CharField(max_length=100)
    experience_years = serializers.IntegerField(default=0)
    consultation_fee = serializers.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'phoneno', 'firstname', 'lastname', 'clinic_center_id', 'license_number', 'experience_years', 'consultation_fee']
    
    def create(self, validated_data):
        clinic_center_id = validated_data.pop('clinic_center_id')
        license_number = validated_data.pop('license_number')
        experience_years = validated_data.pop('experience_years')
        consultation_fee = validated_data.pop('consultation_fee')
        
        # Create user with doctor user type
        user = User.objects.create(**validated_data)
        
        try:
            doctor_type = UserType.objects.get(name='doctor')
            user.usertype = doctor_type
        except UserType.DoesNotExist:
            doctor_type = UserType.objects.create(name='doctor')
            user.usertype = doctor_type
        
        user.save()
        
        # Create DoctorProfile
        from account.models import EClinicCenter, DoctorProfile
        try:
            clinic_center = EClinicCenter.objects.get(id=clinic_center_id)
            DoctorProfile.objects.create(
                account=user,
                clinic_center=clinic_center,
                license_number=license_number,
                experience_years=experience_years,
                consultation_fee=consultation_fee
            )
        except EClinicCenter.DoesNotExist:
            raise serializers.ValidationError("Clinic center not found")
        
        return user

















