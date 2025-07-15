from django.db import models
from account.models import Account, PatientProfile, DoctorProfile, EClinicCenter

class MedicalRecord(models.Model):
    """Model for Patient Medical Records"""
    RECORD_TYPE_CHOICES = [
        ('diagnosis', 'Diagnosis'),
        ('treatment', 'Treatment'),
        ('prescription', 'Prescription'),
        ('lab_result', 'Lab Result'),
        ('imaging', 'Imaging'),
        ('surgery', 'Surgery'),
        ('vaccination', 'Vaccination'),
        ('allergy', 'Allergy'),
        ('family_history', 'Family History'),
        ('other', 'Other'),
    ]
    
    patient = models.ForeignKey(PatientProfile, on_delete=models.CASCADE, related_name='medical_records')
    doctor = models.ForeignKey(DoctorProfile, on_delete=models.CASCADE, related_name='created_medical_records')
    clinic_center = models.ForeignKey(EClinicCenter, on_delete=models.CASCADE, related_name='medical_records')
    record_type = models.CharField(max_length=20, choices=RECORD_TYPE_CHOICES, default='other')
    title = models.CharField(max_length=200)
    description = models.TextField(max_length=5000, null=True, blank=True)
    diagnosis = models.TextField(max_length=2000, null=True, blank=True)
    treatment = models.TextField(max_length=2000, null=True, blank=True)
    medications = models.TextField(max_length=1000, null=True, blank=True)
    dosage = models.CharField(max_length=100, null=True, blank=True)
    duration = models.CharField(max_length=100, null=True, blank=True)
    date_of_record = models.DateField()
    next_follow_up = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.patient.account.firstname} - {self.title} ({self.record_type})"
    
    class Meta:
        ordering = ['-date_of_record', '-created_at']

class PatientDocument(models.Model):
    """Model for Patient Documents"""
    DOCUMENT_TYPE_CHOICES = [
        ('id_proof', 'ID Proof'),
        ('insurance', 'Insurance'),
        ('medical_report', 'Medical Report'),
        ('prescription', 'Prescription'),
        ('lab_report', 'Lab Report'),
        ('xray', 'X-Ray'),
        ('mri', 'MRI'),
        ('ct_scan', 'CT Scan'),
        ('ultrasound', 'Ultrasound'),
        ('discharge_summary', 'Discharge Summary'),
        ('consent_form', 'Consent Form'),
        ('other', 'Other'),
    ]
    
    patient = models.ForeignKey(PatientProfile, on_delete=models.CASCADE, related_name='documents')
    uploaded_by = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='uploaded_documents')
    clinic_center = models.ForeignKey(EClinicCenter, on_delete=models.CASCADE, related_name='patient_documents')
    document_type = models.CharField(max_length=20, choices=DOCUMENT_TYPE_CHOICES, default='other')
    title = models.CharField(max_length=200)
    description = models.TextField(max_length=1000, null=True, blank=True)
    file = models.FileField(upload_to='patient_documents/')
    file_size = models.IntegerField(null=True, blank=True)  # Size in bytes
    file_type = models.CharField(max_length=50, null=True, blank=True)  # MIME type
    is_verified = models.BooleanField(default=False)
    verified_by = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, blank=True, related_name='verified_documents')
    verified_at = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.patient.account.firstname} - {self.title} ({self.document_type})"
    
    class Meta:
        ordering = ['-created_at']
    
    def save(self, *args, **kwargs):
        if self.file:
            self.file_size = self.file.size
            self.file_type = self.file.content_type
        super().save(*args, **kwargs)

class PatientNote(models.Model):
    """Model for Patient Notes"""
    NOTE_TYPE_CHOICES = [
        ('general', 'General'),
        ('symptom', 'Symptom'),
        ('medication', 'Medication'),
        ('allergy', 'Allergy'),
        ('lifestyle', 'Lifestyle'),
        ('family_history', 'Family History'),
        ('social_history', 'Social History'),
        ('other', 'Other'),
    ]
    
    patient = models.ForeignKey(PatientProfile, on_delete=models.CASCADE, related_name='notes')
    created_by = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='created_notes')
    clinic_center = models.ForeignKey(EClinicCenter, on_delete=models.CASCADE, related_name='patient_notes')
    note_type = models.CharField(max_length=20, choices=NOTE_TYPE_CHOICES, default='general')
    title = models.CharField(max_length=200)
    content = models.TextField(max_length=5000)
    is_important = models.BooleanField(default=False)
    is_private = models.BooleanField(default=False)  # Only visible to creator
    tags = models.CharField(max_length=500, null=True, blank=True)  # Comma-separated tags
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.patient.account.firstname} - {self.title} ({self.note_type})"
    
    class Meta:
        ordering = ['-created_at']
