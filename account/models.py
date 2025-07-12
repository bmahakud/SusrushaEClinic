from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
import datetime
from django.utils import timezone



class MyAccountManager(BaseUserManager):
    def create_user(self, username=None, email=None, phone_number=None, password=None):
        if not username and not email and not phone_number:
            raise ValueError("At least one of username, email, or phone number must be provided.")

        user = self.model(
            username=username,
            email=self.normalize_email(email) if email else None,
            phoneno=phone_number
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, username, password):
        user = self.create_user(
            password=password,
            username=username,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user







def get_default_profile_image():
	return "defaults/default_profile.png"



class UserType(models.Model):
    USER_TYPE_CHOICES = [
        ('super_admin', 'Super Admin'),
        ('clinic_admin', 'Clinic Admin'),
        ('doctor', 'Doctor'),
        ('patient', 'Patient'),
    ]
    
    name = models.CharField(max_length=50, choices=USER_TYPE_CHOICES, unique=True)
    
    def __str__(self):
        return self.name + "-Id: " + str(self.id)
    
    class Meta:
        ordering = ['name']








 








        








class Account(AbstractBaseUser, PermissionsMixin):
    # Basic user information
    firstname = models.CharField(verbose_name="firstname", max_length=50, default="", blank=True)
    lastname = models.CharField(verbose_name="lastname", max_length=50, default="", blank=True)
    email = models.EmailField(verbose_name="email", max_length=60, null=True, default=None, blank=True)
    username = models.CharField(max_length=200, unique=True, null=True)
    phoneno = models.CharField(max_length=20, unique=True, null=True)
    
    # User type and permissions
    usertype = models.ForeignKey(UserType, on_delete=models.CASCADE, null=True, default=None)
    date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    
    # Profile information
    profile_image = models.ImageField(max_length=255, upload_to='profile_images/', null=True, blank=True, default=get_default_profile_image)
    gender = models.CharField(verbose_name="gender", max_length=20, default="", blank=True)
    dateofbirth = models.DateField(verbose_name="dob", default=datetime.date.today, null=True, blank=True)
    
    # Address information
    address = models.TextField(max_length=500, null=True, blank=True)
    city = models.CharField(verbose_name="city", max_length=100, default="", blank=True)
    state = models.CharField(verbose_name="state", max_length=100, default="", blank=True)
    country = models.CharField(verbose_name="country", max_length=100, default="", blank=True)
    pincode = models.CharField(max_length=20, null=True, blank=True)
    
    # Additional information
    about = models.TextField(max_length=2000, null=True, blank=True)
    
    # OTP field for authentication
    temp_otp = models.CharField(max_length=6, null=True, blank=True)
    otp_created_at = models.DateTimeField(null=True, blank=True)



    USERNAME_FIELD = 'username';
    REQUIRED_FIELDS = [];
    objects = MyAccountManager()

    def __str__(self):
       return self.email or self.phoneno or "Unnamed"


    
    # E-Clinic System Methods
    def is_super_admin(self):
        return self.usertype and self.usertype.name == 'super_admin'
    
    def is_clinic_admin(self):
        return self.usertype and self.usertype.name == 'clinic_admin'
    
    def is_doctor(self):
        return self.usertype and self.usertype.name == 'doctor'
    
    def is_patient(self):
        return self.usertype and self.usertype.name == 'patient'
    
    def get_clinic_center(self):
        """Get the clinic center associated with this user"""
        if self.is_doctor() and hasattr(self, 'doctor_profile'):
            return self.doctor_profile.clinic_center
        elif self.is_clinic_admin() and hasattr(self, 'admin_profile'):
            return self.admin_profile.clinic_center
        elif self.is_patient() and hasattr(self, 'patient_profile'):
            return self.patient_profile.clinic_center
        return None
    
    # For checking permissions. to keep it simple all admin have ALL permissons
    def has_perm(self, perm, obj=None):
       return self.is_admin
    # Does this user have permission to view this app? (ALWAYS YES FOR SIMPLICITY)
    def has_module_perms(self, app_label):
       return True





# E-Clinic System Models

class EClinicCenter(models.Model):
    """Model for E-Clinic Centers created by Super Admin"""
    name = models.CharField(max_length=300, null=True, blank=True)
    clinic_id = models.CharField(max_length=50, unique=True, null=True, blank=True)
    address = models.TextField(max_length=1000, null=True, blank=True)
    city = models.CharField(max_length=200, null=True, blank=True)
    state = models.CharField(max_length=200, null=True, blank=True)
    country = models.CharField(max_length=200, null=True, blank=True)
    pincode = models.CharField(max_length=20, null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(max_length=100, null=True, blank=True)
    website = models.URLField(max_length=200, null=True, blank=True)
    logo = models.ImageField(upload_to='clinic_logos/', null=True, blank=True)
    description = models.TextField(max_length=5000, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} - {self.clinic_id}"
    
    class Meta:
        ordering = ['name']

class DoctorSpecialization(models.Model):
    """Model for Doctor Specializations"""
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField(max_length=1000, null=True, blank=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']

class DoctorProfile(models.Model):
    """Extended profile for Doctors"""
    account = models.OneToOneField('Account', on_delete=models.CASCADE, related_name='doctor_profile')
    clinic_center = models.ForeignKey(EClinicCenter, on_delete=models.CASCADE, related_name='doctors')
    specializations = models.ManyToManyField(DoctorSpecialization, blank=True)
    license_number = models.CharField(max_length=100, unique=True, null=True, blank=True)
    experience_years = models.IntegerField(default=0)
    consultation_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    available_days = models.CharField(max_length=100, default="Monday,Tuesday,Wednesday,Thursday,Friday")
    available_hours = models.CharField(max_length=100, default="09:00-17:00")
    is_available = models.BooleanField(default=True)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    total_reviews = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Dr. {self.account.firstname} {self.account.lastname} - {self.clinic_center.name}"

class AdminProfile(models.Model):
    """Extended profile for Clinic Admins"""
    account = models.OneToOneField('Account', on_delete=models.CASCADE, related_name='admin_profile')
    clinic_center = models.ForeignKey(EClinicCenter, on_delete=models.CASCADE, related_name='admins')
    role = models.CharField(max_length=100, default="Admin")  # Admin, Manager, etc.
    permissions = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.account.firstname} {self.account.lastname} - {self.clinic_center.name}"

class PatientProfile(models.Model):
    """Extended profile for Patients"""
    account = models.OneToOneField('Account', on_delete=models.CASCADE, related_name='patient_profile')
    clinic_center = models.ForeignKey(EClinicCenter, on_delete=models.CASCADE, related_name='patients')
    patient_id = models.CharField(max_length=50, unique=True, null=True, blank=True)
    emergency_contact_name = models.CharField(max_length=100, null=True, blank=True)
    emergency_contact_phone = models.CharField(max_length=20, null=True, blank=True)
    emergency_contact_relation = models.CharField(max_length=50, null=True, blank=True)
    blood_group = models.CharField(max_length=10, null=True, blank=True)
    allergies = models.TextField(max_length=1000, null=True, blank=True)
    medical_history = models.TextField(max_length=5000, null=True, blank=True)
    current_medications = models.TextField(max_length=1000, null=True, blank=True)
    insurance_provider = models.CharField(max_length=100, null=True, blank=True)
    insurance_number = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.account.firstname} {self.account.lastname} - {self.patient_id}"

class AppointmentSlot(models.Model):
    """Model for Doctor Appointment Slots"""
    doctor = models.ForeignKey(DoctorProfile, on_delete=models.CASCADE, related_name='appointment_slots')
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_available = models.BooleanField(default=True)
    is_booked = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.doctor.account.firstname} - {self.date} {self.start_time}"
    
    class Meta:
        ordering = ['date', 'start_time']
        unique_together = ['doctor', 'date', 'start_time']

class Appointment(models.Model):
    """Model for Patient Appointments"""
    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('no_show', 'No Show'),
    ]
    
    patient = models.ForeignKey(PatientProfile, on_delete=models.CASCADE, related_name='appointments')
    doctor = models.ForeignKey(DoctorProfile, on_delete=models.CASCADE, related_name='appointments')
    slot = models.ForeignKey(AppointmentSlot, on_delete=models.CASCADE, related_name='appointments')
    clinic_center = models.ForeignKey(EClinicCenter, on_delete=models.CASCADE, related_name='appointments')
    appointment_id = models.CharField(max_length=50, unique=True, null=True, blank=True)
    reason = models.TextField(max_length=1000, null=True, blank=True)
    symptoms = models.TextField(max_length=1000, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')
    notes = models.TextField(max_length=2000, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.appointment_id} - {self.patient.account.firstname} with Dr. {self.doctor.account.firstname}"
    
    class Meta:
        ordering = ['-created_at']






