# Profile Management API Documentation

This document describes the API endpoints for user profile management in the Sushru Backend system.

## Base URL
```
https://hellotoppers.com/api/
```

## Authentication
All endpoints (except registration and OTP) require JWT authentication. Include the token in the Authorization header:
```
Authorization: JWT <your_access_token>
```

## Endpoints

### 1. Get My Profile
**GET** `/profile/`

Get the current authenticated user's profile information.

**Headers:**
```
Authorization: JWT <access_token>
```

**Response:**
```json
{
    "id": 1,
    "firstname": "John",
    "lastname": "Doe",
    "email": "john.doe@example.com",
    "username": "user_1234567890",
    "phoneno": "1234567890",
    "about": "About me...",
    "usertype": {
        "id": 4,
        "name": "patient"
    },
    "profile_image": "https://example.com/media/profile_images/user.jpg",
    "gender": "Male",
    "dateofbirth": "1990-01-01",
    "address": "123 Main St",
    "city": "New York",
    "state": "NY",
    "country": "USA"
}
```

### 2. Update My Profile
**PUT** `/profile/update/`

Update the current authenticated user's profile information.

**Headers:**
```
Authorization: JWT <access_token>
Content-Type: application/json
```

**Request Body:**
```json
{
    "firstname": "John",
    "lastname": "Doe",
    "email": "john.doe@example.com",
    "about": "Updated about me...",
    "gender": "Male",
    "dateofbirth": "1990-01-01",
    "address": "123 Main St",
    "city": "New York",
    "state": "NY",
    "country": "USA",
    "pincode": "10001"
}
```

**Response:**
```json
{
    "message": "Profile updated successfully",
    "profile": {
        "id": 1,
        "firstname": "John",
        "lastname": "Doe",
        "email": "john.doe@example.com",
        "username": "user_1234567890",
        "phoneno": "1234567890",
        "about": "Updated about me...",
        "usertype": {
            "id": 4,
            "name": "patient"
        },
        "profile_image": "https://example.com/media/profile_images/user.jpg",
        "gender": "Male",
        "dateofbirth": "1990-01-01",
        "address": "123 Main St",
        "city": "New York",
        "state": "NY",
        "country": "USA"
    }
}
```

### 3. Upload Profile Photo
**POST** `/profile/upload-photo/`

Upload a profile picture for the current authenticated user.

**Headers:**
```
Authorization: JWT <access_token>
Content-Type: multipart/form-data
```

**Request Body:**
```
profile_image: <file>
```

**Response:**
```json
{
    "message": "Profile photo uploaded successfully",
    "profile_image": "https://example.com/media/profile_images/new_photo.jpg"
}
```

### 4. List Patients
**GET** `/patients/`

Get all patients with pagination and filtering options.

**Headers:**
```
Authorization: JWT <access_token>
```

**Query Parameters:**
- `page`: Page number (default: 1)
- `page_size`: Items per page (default: 20)
- `search`: Search in firstname, lastname, email, username, phoneno
- `is_active`: Filter by active status (true/false)
- `city`: Filter by city
- `state`: Filter by state
- `country`: Filter by country
- `ordering`: Sort by field (e.g., firstname, lastname, date_joined)

**Example Request:**
```
GET /patients/?search=john&city=New York&ordering=firstname&page=1
```

**Response:**
```json
{
    "count": 150,
    "next": "https://hellotoppers.com/api/patients/?page=2",
    "previous": null,
    "results": [
        {
            "id": 1,
            "firstname": "John",
            "lastname": "Doe",
            "email": "john.doe@example.com",
            "username": "user_1234567890",
            "phoneno": "1234567890",
            "usertype": 4,
            "usertype_name": "patient",
            "profile_image": "https://example.com/media/profile_images/user.jpg",
            "is_active": true,
            "date_joined": "2024-01-01T10:00:00Z"
        }
    ]
}
```

### 5. List Doctors
**GET** `/doctors/`

Get all doctors with pagination and filtering options.

**Headers:**
```
Authorization: JWT <access_token>
```

**Query Parameters:**
- `page`: Page number (default: 1)
- `page_size`: Items per page (default: 20)
- `search`: Search in firstname, lastname, email, username, phoneno
- `is_active`: Filter by active status (true/false)
- `city`: Filter by city
- `state`: Filter by state
- `country`: Filter by country
- `ordering`: Sort by field (e.g., firstname, lastname, date_joined)

**Example Request:**
```
GET /doctors/?search=dr&city=New York&ordering=lastname&page=1
```

**Response:**
```json
{
    "count": 25,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 2,
            "firstname": "Dr. Jane",
            "lastname": "Smith",
            "email": "jane.smith@clinic.com",
            "username": "dr_jane_smith",
            "phoneno": "9876543210",
            "usertype": 3,
            "usertype_name": "doctor",
            "profile_image": "https://example.com/media/profile_images/doctor.jpg",
            "is_active": true,
            "date_joined": "2024-01-15T09:00:00Z"
        }
    ]
}
```

### 6. List Admins
**GET** `/admins/`

Get all clinic admins with pagination and filtering options.

**Headers:**
```
Authorization: JWT <access_token>
```

**Query Parameters:**
- `page`: Page number (default: 1)
- `page_size`: Items per page (default: 20)
- `search`: Search in firstname, lastname, email, username, phoneno
- `is_active`: Filter by active status (true/false)
- `city`: Filter by city
- `state`: Filter by state
- `country`: Filter by country
- `ordering`: Sort by field (e.g., firstname, lastname, date_joined)

**Example Request:**
```
GET /admins/?search=admin&is_active=true&ordering=date_joined&page=1
```

**Response:**
```json
{
    "count": 10,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 3,
            "firstname": "Admin",
            "lastname": "User",
            "email": "admin@clinic.com",
            "username": "admin_user",
            "phoneno": "5555555555",
            "usertype": 2,
            "usertype_name": "clinic_admin",
            "profile_image": "https://example.com/media/profile_images/admin.jpg",
            "is_active": true,
            "date_joined": "2024-01-10T08:00:00Z"
        }
    ]
}
```

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

## User Types

The system supports the following user types:
- `super_admin`: Super administrator with full system access
- `clinic_admin`: Clinic administrator with clinic-specific access
- `doctor`: Medical doctor with patient management access
- `patient`: Patient with personal profile access

## File Upload

For profile photo uploads:
- Supported formats: JPG, PNG, GIF
- Maximum file size: 5MB
- Files are stored in the `profile_images/` directory
- URLs are returned as absolute paths

## Pagination

All list endpoints support pagination with the following parameters:
- `page`: Page number (starts from 1)
- `page_size`: Number of items per page (default: 20, max: 100)

## Filtering and Search

List endpoints support:
- **Search**: Text search across multiple fields
- **Filtering**: Filter by specific field values
- **Ordering**: Sort results by any field in ascending or descending order

## Rate Limiting

API endpoints are subject to rate limiting to prevent abuse. Please implement appropriate retry logic in your applications. 