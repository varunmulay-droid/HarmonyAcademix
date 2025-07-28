import random
import string
from datetime import datetime
from app import db
from flask_login import UserMixin
from sqlalchemy import func

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256))
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Student specific fields
    stu_id = db.Column(db.String(10), unique=True, nullable=True)
    first_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64))
    phone = db.Column(db.String(20))
    
    # Relationships
    admission_forms = db.relationship('AdmissionForm', backref='student', lazy=True)
    bonafide_requests = db.relationship('BonafideRequest', backref='student', lazy=True)
    hostel_applications = db.relationship('HostelApplication', backref='student', lazy=True)
    case_records = db.relationship('CaseRecord', backref='student', lazy=True)
    pratinidhan_forms = db.relationship('PratinidhanForm', backref='student', lazy=True)

    def generate_stu_id(self):
        """Generate unique STU ID in format STU001-STU300"""
        if self.stu_id:
            return self.stu_id
            
        for i in range(1, 301):  # STU001 to STU300
            stu_id = f"STU{i:03d}"
            if not User.query.filter_by(stu_id=stu_id).first():
                self.stu_id = stu_id
                return stu_id
        
        # If all STU IDs are taken, generate random one
        while True:
            stu_id = f"STU{random.randint(301, 999):03d}"
            if not User.query.filter_by(stu_id=stu_id).first():
                self.stu_id = stu_id
                return stu_id

class AdmissionForm(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    form_number = db.Column(db.String(20))
    
    # School information
    school_name = db.Column(db.String(200))
    student_continuous_id = db.Column(db.String(50))
    udise_pen = db.Column(db.String(50))
    admission_class = db.Column(db.String(20))
    
    # Personal information
    birth_register_no = db.Column(db.String(50))
    aadhar_no = db.Column(db.String(20))
    birth_date = db.Column(db.Date)
    admission_date = db.Column(db.Date)
    gender = db.Column(db.String(10))
    
    # Names
    first_name_marathi = db.Column(db.String(100))
    last_name_marathi = db.Column(db.String(100))
    father_name = db.Column(db.String(100))
    mother_name = db.Column(db.String(100))
    
    # Additional details
    birth_date_words = db.Column(db.String(200))
    religion = db.Column(db.String(50))
    caste = db.Column(db.String(50))
    subcaste = db.Column(db.String(50))
    caste_certificate = db.Column(db.String(100))
    is_minority = db.Column(db.Boolean)
    nationality = db.Column(db.String(50))
    mother_tongue = db.Column(db.String(50))
    mobile_number = db.Column(db.String(20))
    
    # Status information
    bpl_status = db.Column(db.Boolean)
    bpl_number = db.Column(db.String(50))
    disability_status = db.Column(db.Boolean)
    disability_type = db.Column(db.String(100))
    
    # Guardian information
    parent_full_name = db.Column(db.String(200))
    address = db.Column(db.Text)
    
    # File uploads
    student_photo = db.Column(db.String(200))
    parent_photo = db.Column(db.String(200))
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='pending')

class BonafideRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    # Student details for certificate
    student_name = db.Column(db.String(200), nullable=False)
    academic_year = db.Column(db.String(20), nullable=False)
    standard = db.Column(db.String(10), nullable=False)
    division = db.Column(db.String(10), nullable=False)
    conduct = db.Column(db.String(50), nullable=False)
    caste = db.Column(db.String(50), nullable=False)
    birth_date = db.Column(db.Date, nullable=False)
    birth_place = db.Column(db.String(100), nullable=False)
    place_of_issue = db.Column(db.String(100), nullable=False)
    student_id = db.Column(db.String(20), nullable=False)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='pending')

class HostelApplication(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    # Application details
    hostel_name = db.Column(db.String(200))
    hostel_address = db.Column(db.Text)
    parent_name = db.Column(db.String(200))
    parent_address = db.Column(db.Text)
    
    # Student information
    student_name = db.Column(db.String(200))
    student_address = db.Column(db.Text)
    phone = db.Column(db.String(20))
    caste = db.Column(db.String(100))
    birth_village = db.Column(db.String(100))
    birth_taluka = db.Column(db.String(100))
    birth_district = db.Column(db.String(100))
    birth_date = db.Column(db.Date)
    age_years = db.Column(db.Integer)
    age_months = db.Column(db.Integer)
    education = db.Column(db.String(200))
    previous_school = db.Column(db.Text)
    annual_income = db.Column(db.String(50))
    exam_results = db.Column(db.Text)
    
    # Agreement details
    guardian_name = db.Column(db.String(200))
    student_agreement_name = db.Column(db.String(200))
    register_number = db.Column(db.String(50))
    received_date = db.Column(db.Date)
    
    # File uploads
    parent_signature = db.Column(db.String(200))
    student_signature = db.Column(db.String(200))
    warden_signature = db.Column(db.String(200))
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='pending')

class CaseRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    # Section 1: Personal Information
    name = db.Column(db.String(200))
    birth_date = db.Column(db.Date)
    age = db.Column(db.Integer)
    gender = db.Column(db.String(20))
    education = db.Column(db.String(200))
    
    # Father's information
    father_name = db.Column(db.String(200))
    father_education = db.Column(db.String(200))
    father_occupation = db.Column(db.String(200))
    father_income = db.Column(db.String(100))
    
    # Mother's information
    mother_name = db.Column(db.String(200))
    mother_education = db.Column(db.String(200))
    mother_occupation = db.Column(db.String(200))
    mother_income = db.Column(db.String(100))
    
    # Guardian's information
    guardian_name = db.Column(db.String(200))
    guardian_education = db.Column(db.String(200))
    guardian_occupation = db.Column(db.String(200))
    guardian_income = db.Column(db.String(100))
    guardian_address = db.Column(db.Text)
    guardian_mobile = db.Column(db.String(20))
    
    # Address information
    relatives_address = db.Column(db.Text)
    permanent_address = db.Column(db.Text)
    
    # Social information
    economic_status = db.Column(db.String(50))
    area_type = db.Column(db.String(50))
    religion = db.Column(db.String(50))
    caste = db.Column(db.String(50))
    mother_tongue = db.Column(db.String(50))
    
    # Section 2: Information provider details
    info_relation_personal = db.Column(db.String(200))
    contact_duration = db.Column(db.String(200))
    info_trustworthiness = db.Column(db.String(50))
    info_completeness = db.Column(db.String(50))
    complaint_details = db.Column(db.Text)
    
    # Past treatment information
    past_treatment_medications = db.Column(db.String(50))
    past_treatment_professional = db.Column(db.String(50))
    past_treatment_physical = db.Column(db.String(50))
    past_treatment_other = db.Column(db.String(200))
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='pending')

class PratinidhanForm(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    # Application details
    application_number = db.Column(db.String(50))
    application_date = db.Column(db.Date)
    
    # Applicant information
    applicant_name = db.Column(db.String(200))
    father_name = db.Column(db.String(200))
    birth_date = db.Column(db.Date)
    birth_place = db.Column(db.String(200))
    permanent_address = db.Column(db.Text)
    current_address = db.Column(db.Text)
    mobile_number = db.Column(db.String(20))
    email = db.Column(db.String(200))
    
    # Educational information
    qualification = db.Column(db.String(200))
    institution_name = db.Column(db.String(200))
    passing_year = db.Column(db.String(10))
    marks_percentage = db.Column(db.String(10))
    
    # Representation details
    representation_type = db.Column(db.String(100))
    organization_name = db.Column(db.String(200))
    designation = db.Column(db.String(100))
    duration = db.Column(db.String(50))
    
    # Documents
    photo = db.Column(db.String(200))
    signature = db.Column(db.String(200))
    qualification_certificate = db.Column(db.String(200))
    experience_certificate = db.Column(db.String(200))
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='pending')
