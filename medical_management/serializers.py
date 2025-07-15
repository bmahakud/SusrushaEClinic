from rest_framework import serializers
from .models import MedicalRecord, PatientDocument, PatientNote
from account.models import Account, UserType
from django.contrib.auth import get_user_model

User = get_user_model()

# Medical Records Serializers
class MedicalRecordSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source='patient.account.firstname', read_only=True)
    doctor_name = serializers.CharField(source='doctor.account.firstname', read_only=True)
    clinic_name = serializers.CharField(source='clinic_center.name', read_only=True)
    
    class Meta:
        model = MedicalRecord
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']

class MedicalRecordCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalRecord
        fields = ['patient', 'clinic_center', 'record_type', 'title', 'description', 'diagnosis', 'treatment', 'medications', 'dosage', 'duration', 'date_of_record', 'next_follow_up']

# Patient Documents Serializers
class PatientDocumentSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source='patient.account.firstname', read_only=True)
    uploaded_by_name = serializers.CharField(source='uploaded_by.firstname', read_only=True)
    verified_by_name = serializers.CharField(source='verified_by.firstname', read_only=True)
    file_url = serializers.SerializerMethodField()
    
    class Meta:
        model = PatientDocument
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at', 'file_size', 'file_type']
    
    def get_file_url(self, obj):
        if obj.file:
            return obj.file.url
        return None

class PatientDocumentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientDocument
        fields = ['patient', 'clinic_center', 'document_type', 'title', 'description', 'file']

class PatientDocumentUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientDocument
        fields = ['title', 'description', 'document_type', 'is_verified']

# Patient Notes Serializers
class PatientNoteSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source='patient.account.firstname', read_only=True)
    created_by_name = serializers.CharField(source='created_by.firstname', read_only=True)
    clinic_name = serializers.CharField(source='clinic_center.name', read_only=True)
    
    class Meta:
        model = PatientNote
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']

class PatientNoteCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientNote
        fields = ['patient', 'clinic_center', 'note_type', 'title', 'content', 'is_important', 'is_private', 'tags']

class PatientNoteUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientNote
        fields = ['title', 'content', 'note_type', 'is_important', 'is_private', 'tags'] 