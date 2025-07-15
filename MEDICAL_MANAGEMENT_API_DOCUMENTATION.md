# Medical Management API Documentation

This document describes the API endpoints for medical records, patient documents, and notes management in the Sushru Backend system.

## Base URL
```
https://hellotoppers.com/api/medical/
```

## Authentication
All endpoints require JWT authentication. Include the token in the Authorization header:
```
Authorization: JWT <your_access_token>
```

## Medical Records APIs

### 1. List Medical Records
**GET** `/medical-records/`

Get all medical records with pagination and filtering.

**Headers:**
```
Authorization: JWT <access_token>
```

**Query Parameters:**
- `patient_id`: Filter by patient ID
- `record_type`: Filter by record type (diagnosis, treatment, prescription, etc.)
- `is_active`: Filter by active status (true/false)
- `patient`: Filter by patient ID
- `doctor`: Filter by doctor ID
- `clinic_center`: Filter by clinic center ID
- `search`: Search in title, description, diagnosis, treatment
- `ordering`: Sort by field (e.g., date_of_record, created_at)
- `page`: Page number (default: 1)
- `page_size`: Items per page (default: 20)

**Example Request:**
```
GET /medical-records/?patient_id=1&record_type=diagnosis&ordering=date_of_record&page=1
```

**Response:**
```json
{
    "count": 15,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "patient": 1,
            "patient_name": "John Doe",
            "doctor": 2,
            "doctor_name": "Dr. Jane Smith",
            "clinic_center": 1,
            "clinic_name": "City Medical Center",
            "record_type": "diagnosis",
            "title": "Hypertension Diagnosis",
            "description": "Patient diagnosed with stage 1 hypertension",
            "diagnosis": "Essential hypertension, stage 1",
            "treatment": "Lifestyle modifications and medication",
            "medications": "Lisinopril 10mg daily",
            "dosage": "10mg",
            "duration": "3 months",
            "date_of_record": "2024-01-15",
            "next_follow_up": "2024-04-15",
            "is_active": true,
            "created_at": "2024-01-15T10:00:00Z",
            "updated_at": "2024-01-15T10:00:00Z"
        }
    ]
}
```

### 2. Create Medical Record
**POST** `/medical-records/`

Create a new medical record (doctors only).

**Headers:**
```
Authorization: JWT <access_token>
Content-Type: application/json
```

**Request Body:**
```json
{
    "patient": 1,
    "clinic_center": 1,
    "record_type": "diagnosis",
    "title": "Hypertension Diagnosis",
    "description": "Patient diagnosed with stage 1 hypertension",
    "diagnosis": "Essential hypertension, stage 1",
    "treatment": "Lifestyle modifications and medication",
    "medications": "Lisinopril 10mg daily",
    "dosage": "10mg",
    "duration": "3 months",
    "date_of_record": "2024-01-15",
    "next_follow_up": "2024-04-15"
}
```

### 3. Get Medical Record
**GET** `/medical-records/{id}/`

Get a specific medical record by ID.

**Headers:**
```
Authorization: JWT <access_token>
```

### 4. Update Medical Record
**PUT** `/medical-records/{id}/`

Update a medical record (doctors only).

**Headers:**
```
Authorization: JWT <access_token>
Content-Type: application/json
```

**Request Body:**
```json
{
    "title": "Updated Hypertension Diagnosis",
    "description": "Updated diagnosis description",
    "treatment": "Updated treatment plan",
    "medications": "Updated medication list",
    "next_follow_up": "2024-05-15"
}
```

### 5. Delete Medical Record
**DELETE** `/medical-records/{id}/`

Delete a medical record (doctors only).

**Headers:**
```
Authorization: JWT <access_token>
```

## Patient Documents APIs

### 6. List Patient Documents
**GET** `/documents/`

Get all patient documents with pagination and filtering.

**Headers:**
```
Authorization: JWT <access_token>
```

**Query Parameters:**
- `patient_id`: Filter by patient ID
- `document_type`: Filter by document type (id_proof, insurance, medical_report, etc.)
- `is_verified`: Filter by verification status (true/false)
- `is_active`: Filter by active status (true/false)
- `patient`: Filter by patient ID
- `clinic_center`: Filter by clinic center ID
- `search`: Search in title, description
- `ordering`: Sort by field (e.g., created_at)
- `page`: Page number (default: 1)
- `page_size`: Items per page (default: 20)

**Example Request:**
```
GET /documents/?patient_id=1&document_type=medical_report&is_verified=true&ordering=created_at&page=1
```

**Response:**
```json
{
    "count": 8,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "patient": 1,
            "patient_name": "John Doe",
            "uploaded_by": 2,
            "uploaded_by_name": "Dr. Jane Smith",
            "clinic_center": 1,
            "clinic_name": "City Medical Center",
            "document_type": "medical_report",
            "title": "Blood Test Report",
            "description": "Complete blood count and lipid profile",
            "file": "/media/patient_documents/blood_test_report.pdf",
            "file_url": "https://example.com/media/patient_documents/blood_test_report.pdf",
            "file_size": 1024000,
            "file_type": "application/pdf",
            "is_verified": true,
            "verified_by": 2,
            "verified_by_name": "Dr. Jane Smith",
            "verified_at": "2024-01-15T11:00:00Z",
            "is_active": true,
            "created_at": "2024-01-15T10:00:00Z",
            "updated_at": "2024-01-15T11:00:00Z"
        }
    ]
}
```

### 7. Upload Patient Document
**POST** `/documents/`

Upload a new patient document.

**Headers:**
```
Authorization: JWT <access_token>
Content-Type: multipart/form-data
```

**Request Body:**
```
patient: 1
clinic_center: 1
document_type: medical_report
title: Blood Test Report
description: Complete blood count and lipid profile
file: <file>
```

### 8. Get Patient Document
**GET** `/documents/{id}/`

Get a specific patient document by ID.

**Headers:**
```
Authorization: JWT <access_token>
```

### 9. Update Patient Document
**PUT** `/documents/{id}/`

Update a patient document.

**Headers:**
```
Authorization: JWT <access_token>
Content-Type: application/json
```

**Request Body:**
```json
{
    "title": "Updated Blood Test Report",
    "description": "Updated description",
    "document_type": "lab_report"
}
```

### 10. Delete Patient Document
**DELETE** `/documents/{id}/`

Delete a patient document.

**Headers:**
```
Authorization: JWT <access_token>
```

### 11. Verify Patient Document
**POST** `/documents/{id}/verify/`

Verify a patient document (doctors and admins only).

**Headers:**
```
Authorization: JWT <access_token>
```

**Response:**
```json
{
    "message": "Document verified successfully",
    "document": {
        "id": 1,
        "patient": 1,
        "patient_name": "John Doe",
        "uploaded_by": 2,
        "uploaded_by_name": "Dr. Jane Smith",
        "clinic_center": 1,
        "clinic_name": "City Medical Center",
        "document_type": "medical_report",
        "title": "Blood Test Report",
        "description": "Complete blood count and lipid profile",
        "file": "/media/patient_documents/blood_test_report.pdf",
        "file_url": "https://example.com/media/patient_documents/blood_test_report.pdf",
        "file_size": 1024000,
        "file_type": "application/pdf",
        "is_verified": true,
        "verified_by": 2,
        "verified_by_name": "Dr. Jane Smith",
        "verified_at": "2024-01-15T11:00:00Z",
        "is_active": true,
        "created_at": "2024-01-15T10:00:00Z",
        "updated_at": "2024-01-15T11:00:00Z"
    }
}
```

## Patient Notes APIs

### 12. List Patient Notes
**GET** `/notes/`

Get all patient notes with pagination and filtering.

**Headers:**
```
Authorization: JWT <access_token>
```

**Query Parameters:**
- `patient_id`: Filter by patient ID
- `note_type`: Filter by note type (general, symptom, medication, etc.)
- `is_important`: Filter by importance (true/false)
- `is_private`: Filter by privacy (true/false)
- `is_active`: Filter by active status (true/false)
- `patient`: Filter by patient ID
- `clinic_center`: Filter by clinic center ID
- `search`: Search in title, content, tags
- `ordering`: Sort by field (e.g., created_at)
- `page`: Page number (default: 1)
- `page_size`: Items per page (default: 20)

**Example Request:**
```
GET /notes/?patient_id=1&note_type=medication&is_important=true&ordering=created_at&page=1
```

**Response:**
```json
{
    "count": 12,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "patient": 1,
            "patient_name": "John Doe",
            "created_by": 2,
            "created_by_name": "Dr. Jane Smith",
            "clinic_center": 1,
            "clinic_name": "City Medical Center",
            "note_type": "medication",
            "title": "Medication Allergy Note",
            "content": "Patient has severe allergy to penicillin. Avoid prescribing any penicillin-based antibiotics.",
            "is_important": true,
            "is_private": false,
            "tags": "allergy,penicillin,medication",
            "is_active": true,
            "created_at": "2024-01-15T10:00:00Z",
            "updated_at": "2024-01-15T10:00:00Z"
        }
    ]
}
```

### 13. Create Patient Note
**POST** `/notes/`

Create a new patient note.

**Headers:**
```
Authorization: JWT <access_token>
Content-Type: application/json
```

**Request Body:**
```json
{
    "patient": 1,
    "clinic_center": 1,
    "note_type": "medication",
    "title": "Medication Allergy Note",
    "content": "Patient has severe allergy to penicillin. Avoid prescribing any penicillin-based antibiotics.",
    "is_important": true,
    "is_private": false,
    "tags": "allergy,penicillin,medication"
}
```

### 14. Get Patient Note
**GET** `/notes/{id}/`

Get a specific patient note by ID.

**Headers:**
```
Authorization: JWT <access_token>
```

### 15. Update Patient Note
**PUT** `/notes/{id}/`

Update a patient note.

**Headers:**
```
Authorization: JWT <access_token>
Content-Type: application/json
```

**Request Body:**
```json
{
    "title": "Updated Medication Allergy Note",
    "content": "Updated content about penicillin allergy",
    "note_type": "allergy",
    "is_important": true,
    "tags": "allergy,penicillin,severe"
}
```

### 16. Delete Patient Note
**DELETE** `/notes/{id}/`

Delete a patient note.

**Headers:**
```
Authorization: JWT <access_token>
```

## Record Types

### Medical Record Types
- `diagnosis`: Medical diagnosis
- `treatment`: Treatment plan
- `prescription`: Medication prescription
- `lab_result`: Laboratory test results
- `imaging`: Imaging results (X-ray, MRI, etc.)
- `surgery`: Surgical procedures
- `vaccination`: Vaccination records
- `allergy`: Allergy information
- `family_history`: Family medical history
- `other`: Other medical records

### Document Types
- `id_proof`: Identity proof documents
- `insurance`: Insurance documents
- `medical_report`: Medical reports
- `prescription`: Prescription documents
- `lab_report`: Laboratory reports
- `xray`: X-ray images
- `mri`: MRI images
- `ct_scan`: CT scan images
- `ultrasound`: Ultrasound images
- `discharge_summary`: Hospital discharge summaries
- `consent_form`: Consent forms
- `other`: Other documents

### Note Types
- `general`: General notes
- `symptom`: Symptom notes
- `medication`: Medication-related notes
- `allergy`: Allergy notes
- `lifestyle`: Lifestyle notes
- `family_history`: Family history notes
- `social_history`: Social history notes
- `other`: Other notes

## Permissions

### Medical Records
- **Create**: Doctors only
- **Read**: Doctors, admins, and patients (their own records)
- **Update**: Doctors only
- **Delete**: Doctors only

### Patient Documents
- **Upload**: Doctors, admins, and patients (their own documents)
- **Read**: Doctors, admins, and patients (their own documents)
- **Update**: Uploader and admins
- **Delete**: Uploader and admins
- **Verify**: Doctors and admins only

### Patient Notes
- **Create**: Doctors, admins, and patients (their own notes)
- **Read**: 
  - Public notes: All authorized users
  - Private notes: Only creator and super admins
- **Update**: Creator and admins
- **Delete**: Creator and admins

## File Upload Guidelines

### Supported File Types
- **Documents**: PDF, DOC, DOCX, TXT
- **Images**: JPG, PNG, GIF, BMP
- **Medical Images**: DICOM files (if supported by your system)

### File Size Limits
- Maximum file size: 10MB per file
- Recommended file size: Under 5MB for better performance

### File Storage
- Files are stored in the `patient_documents/` directory
- File metadata (size, type) is automatically captured
- File URLs are returned as absolute paths

## Error Responses

### 400 Bad Request
```json
{
    "field_name": ["Error message"]
}
```

### 401 Unauthorized
```json
{
    "detail": "Authentication credentials were not provided."
}
```

### 403 Forbidden
```json
{
    "detail": "You do not have permission to perform this action."
}
```

### 404 Not Found
```json
{
    "detail": "Not found."
}
```

### 413 Payload Too Large
```json
{
    "detail": "File size exceeds maximum allowed size."
}
```

## Rate Limiting

API endpoints are subject to rate limiting to prevent abuse:
- Document upload: 10 uploads per minute
- Note creation: 50 notes per minute
- Medical record creation: 20 records per minute

Please implement appropriate retry logic in your applications.

## Best Practices

1. **File Uploads**: Compress large files before upload
2. **Notes**: Use appropriate tags for better organization
3. **Privacy**: Mark sensitive notes as private when appropriate
4. **Verification**: Verify important documents promptly
5. **Pagination**: Always use pagination for large datasets
6. **Search**: Use specific search terms and filters to improve performance 