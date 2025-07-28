# Project Harmony Hands - Student ERP System

## Overview

Project Harmony Hands is a web-based Student ERP (Enterprise Resource Planning) system designed for educational institutions. The application is built using Flask (Python) and provides comprehensive student management functionality including admission forms, bonafide certificates, hostel applications, and case records. The system supports both English and Marathi languages, with a focus on Marathi language support for Indian educational institutions.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

The application follows a traditional Flask web application architecture with the following key characteristics:

### Backend Architecture
- **Framework**: Flask (Python web framework)
- **Database ORM**: Flask-SQLAlchemy with SQLAlchemy Core
- **Authentication**: Flask-Login for session management
- **File Handling**: Werkzeug for secure file uploads
- **Template Engine**: Jinja2 (Flask's default)

### Frontend Architecture
- **CSS Framework**: Bootstrap 5.3.3 for responsive design
- **Icons**: Font Awesome 6.0.0 for UI icons
- **Fonts**: Google Fonts (Noto Sans Devanagari) for Marathi text support
- **JavaScript**: Vanilla JavaScript with Bootstrap components

### Database Design
- **Primary Database**: SQLite (default), configurable to other databases via DATABASE_URL
- **ORM Pattern**: Declarative Base with Flask-SQLAlchemy
- **Connection Management**: Pool recycling and pre-ping for reliability

## Key Components

### User Management
- **User Model**: Handles both students and administrators
- **Authentication**: Password hashing with Werkzeug security
- **Student ID Generation**: Automatic STU ID assignment (STU001-STU300 range)
- **Role-based Access**: Admin and student user types

### Form Management System
The system provides multiple form types:
1. **Admission Forms**: School admission applications
2. **Bonafide Certificates**: Student verification documents
3. **Hostel Applications**: Accommodation requests
4. **Case Records**: Student counseling/case management
5. **Pratinidhan Forms**: Representative certificates

### File Upload System
- **Upload Directory**: Configurable upload folder
- **File Size Limit**: 16MB maximum file size
- **Security**: Secure filename handling with allowed extensions
- **Supported Formats**: PNG, JPG, JPEG, GIF, PDF

### Dashboard System
- **Student Dashboard**: Personal form management and statistics
- **Admin Dashboard**: System-wide management and reporting
- **Statistics**: Real-time counts of students and applications

## Data Flow

### User Registration Flow
1. User registers with personal details
2. System assigns unique STU ID automatically
3. User credentials are hashed and stored
4. User can access student dashboard

### Form Submission Flow
1. Student selects form type from dashboard
2. Form data is submitted via POST request
3. System validates and stores form data
4. Admin can review and manage submissions

### Authentication Flow
1. User provides username/password
2. System verifies credentials against database
3. Flask-Login manages session state
4. Role-based redirection to appropriate dashboard

## External Dependencies

### Python Packages
- **Flask**: Web framework core
- **Flask-SQLAlchemy**: Database ORM
- **Flask-Login**: Authentication management
- **Werkzeug**: WSGI utilities and security

### Frontend Libraries
- **Bootstrap 5.3.3**: UI framework (CDN)
- **Font Awesome 6.0.0**: Icon library (CDN)
- **Google Fonts**: Noto Sans Devanagari for Marathi support

### Development Tools
- **ProxyFix**: WSGI middleware for reverse proxy support
- **Logging**: Python built-in logging for debugging

## Deployment Strategy

### Environment Configuration
- **Secret Key**: Configurable via SESSION_SECRET environment variable
- **Database URL**: Configurable via DATABASE_URL environment variable
- **Debug Mode**: Enabled for development, should be disabled in production

### File System Requirements
- **Upload Directory**: Automatically created on startup
- **Static Files**: CSS, JavaScript, and image assets
- **Template Directory**: Jinja2 templates for all pages

### Production Considerations
- **Database**: Currently uses SQLite, easily configurable for PostgreSQL or MySQL
- **File Storage**: Local file system, can be extended for cloud storage
- **Security**: ProxyFix middleware configured for reverse proxy deployment
- **Logging**: Debug level logging enabled (should be adjusted for production)

### Scalability Notes
- **Database Connection Pooling**: Configured with pool recycling and pre-ping
- **Session Management**: Flask-Login with server-side sessions
- **Static Asset Delivery**: Can be offloaded to CDN or web server

The application is designed for easy deployment on platforms like Replit, with minimal configuration required for basic functionality. The modular structure allows for easy extension and customization of forms and features.