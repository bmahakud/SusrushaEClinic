from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.utils import timezone

from .models import MedicalRecord, PatientDocument, PatientNote
from .serializers import (
    MedicalRecordSerializer, MedicalRecordCreateSerializer,
    PatientDocumentSerializer, PatientDocumentCreateSerializer, PatientDocumentUpdateSerializer,
    PatientNoteSerializer, PatientNoteCreateSerializer, PatientNoteUpdateSerializer
)

# Medical Records Views
class MedicalRecordListView(generics.ListCreateAPIView):
    serializer_class = MedicalRecordSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['record_type', 'is_active', 'patient', 'doctor', 'clinic_center']
    search_fields = ['title', 'description', 'diagnosis', 'treatment']
    ordering_fields = ['date_of_record', 'created_at']
    ordering = ['-date_of_record']
    
    def get_queryset(self):
        """Get medical records with filtering"""
        queryset = MedicalRecord.objects.all()
        
        # Filter by patient if specified
        patient_id = self.request.query_params.get('patient_id', None)
        if patient_id:
            queryset = queryset.filter(patient_id=patient_id)
        
        # Filter by clinic center if user is not super admin
        if not self.request.user.is_super_admin():
            clinic_center = self.request.user.get_clinic_center()
            if clinic_center:
                queryset = queryset.filter(clinic_center=clinic_center)
        
        return queryset
    
    def perform_create(self, serializer):
        """Create medical record with doctor info"""
        serializer.save(doctor=self.request.user.doctor_profile)

class MedicalRecordDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = MedicalRecordSerializer
    permission_classes = [IsAuthenticated]
    queryset = MedicalRecord.objects.all()
    
    def get_queryset(self):
        """Filter by clinic center if user is not super admin"""
        queryset = MedicalRecord.objects.all()
        if not self.request.user.is_super_admin():
            clinic_center = self.request.user.get_clinic_center()
            if clinic_center:
                queryset = queryset.filter(clinic_center=clinic_center)
        return queryset

# Patient Documents Views
class PatientDocumentListView(generics.ListCreateAPIView):
    serializer_class = PatientDocumentSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['document_type', 'is_verified', 'is_active', 'patient', 'clinic_center']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at']
    ordering = ['-created_at']
    
    def get_queryset(self):
        """Get patient documents with filtering"""
        queryset = PatientDocument.objects.all()
        
        # Filter by patient if specified
        patient_id = self.request.query_params.get('patient_id', None)
        if patient_id:
            queryset = queryset.filter(patient_id=patient_id)
        
        # Filter by clinic center if user is not super admin
        if not self.request.user.is_super_admin():
            clinic_center = self.request.user.get_clinic_center()
            if clinic_center:
                queryset = queryset.filter(clinic_center=clinic_center)
        
        return queryset
    
    def perform_create(self, serializer):
        """Create document with uploader info"""
        serializer.save(uploaded_by=self.request.user)

class PatientDocumentDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PatientDocumentSerializer
    permission_classes = [IsAuthenticated]
    queryset = PatientDocument.objects.all()
    
    def get_queryset(self):
        """Filter by clinic center if user is not super admin"""
        queryset = PatientDocument.objects.all()
        if not self.request.user.is_super_admin():
            clinic_center = self.request.user.get_clinic_center()
            if clinic_center:
                queryset = queryset.filter(clinic_center=clinic_center)
        return queryset

class VerifyDocumentView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request, pk):
        """Verify a patient document"""
        document = get_object_or_404(PatientDocument, pk=pk)
        
        # Check permissions (only doctors and admins can verify)
        if not (request.user.is_doctor() or request.user.is_clinic_admin() or request.user.is_super_admin()):
            return Response({
                'error': 'Only doctors and admins can verify documents'
            }, status=status.HTTP_403_FORBIDDEN)
        
        document.is_verified = True
        document.verified_by = request.user
        document.verified_at = timezone.now()
        document.save()
        
        return Response({
            'message': 'Document verified successfully',
            'document': PatientDocumentSerializer(document).data
        }, status=status.HTTP_200_OK)

# Patient Notes Views
class PatientNoteListView(generics.ListCreateAPIView):
    serializer_class = PatientNoteSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['note_type', 'is_important', 'is_private', 'is_active', 'patient', 'clinic_center']
    search_fields = ['title', 'content', 'tags']
    ordering_fields = ['created_at']
    ordering = ['-created_at']
    
    def get_queryset(self):
        """Get patient notes with filtering"""
        queryset = PatientNote.objects.all()
        
        # Filter by patient if specified
        patient_id = self.request.query_params.get('patient_id', None)
        if patient_id:
            queryset = queryset.filter(patient_id=patient_id)
        
        # Filter private notes (only show to creator)
        if not self.request.user.is_super_admin():
            queryset = queryset.filter(
                Q(is_private=False) | Q(created_by=self.request.user)
            )
        
        # Filter by clinic center if user is not super admin
        if not self.request.user.is_super_admin():
            clinic_center = self.request.user.get_clinic_center()
            if clinic_center:
                queryset = queryset.filter(clinic_center=clinic_center)
        
        return queryset
    
    def perform_create(self, serializer):
        """Create note with creator info"""
        serializer.save(created_by=self.request.user)

class PatientNoteDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PatientNoteSerializer
    permission_classes = [IsAuthenticated]
    queryset = PatientNote.objects.all()
    
    def get_queryset(self):
        """Filter by clinic center and private notes"""
        queryset = PatientNote.objects.all()
        
        # Filter private notes (only show to creator)
        if not self.request.user.is_super_admin():
            queryset = queryset.filter(
                Q(is_private=False) | Q(created_by=self.request.user)
            )
        
        # Filter by clinic center if user is not super admin
        if not self.request.user.is_super_admin():
            clinic_center = self.request.user.get_clinic_center()
            if clinic_center:
                queryset = queryset.filter(clinic_center=clinic_center)
        
        return queryset
