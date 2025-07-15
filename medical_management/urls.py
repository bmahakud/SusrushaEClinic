from django.urls import path
from .views import (
    MedicalRecordListView, MedicalRecordDetailView,
    PatientDocumentListView, PatientDocumentDetailView, VerifyDocumentView,
    PatientNoteListView, PatientNoteDetailView
)

app_name = 'medical_management'

urlpatterns = [
    # Medical Records
    path('medical-records/', MedicalRecordListView.as_view(), name='medical-records-list'),
    path('medical-records/<int:pk>/', MedicalRecordDetailView.as_view(), name='medical-record-detail'),
    
    # Patient Documents
    path('documents/', PatientDocumentListView.as_view(), name='documents-list'),
    path('documents/<int:pk>/', PatientDocumentDetailView.as_view(), name='document-detail'),
    path('documents/<int:pk>/verify/', VerifyDocumentView.as_view(), name='verify-document'),
    
    # Patient Notes
    path('notes/', PatientNoteListView.as_view(), name='notes-list'),
    path('notes/<int:pk>/', PatientNoteDetailView.as_view(), name='note-detail'),
] 