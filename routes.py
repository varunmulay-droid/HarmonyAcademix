import os
from datetime import datetime
from flask import render_template, request, redirect, url_for, flash, session, jsonify, send_file
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from app import app, db
from models import User, AdmissionForm, BonafideRequest, HostelApplication, CaseRecord, PratinidhanForm

def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            if user.is_admin:
                return redirect(url_for('admin_dashboard'))
            else:
                # Generate STU ID if not exists
                if not user.stu_id:
                    user.generate_stu_id()
                    db.session.commit()
                return redirect(url_for('student_dashboard'))
        else:
            flash('अवैध उपयोगकर्ता नाव किंवा पासवर्ड', 'error')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        phone = request.form['phone']
        
        # Validation
        if password != confirm_password:
            flash('पासवर्ड जुळत नाहीत', 'error')
            return render_template('register.html')
        
        if User.query.filter_by(username=username).first():
            flash('हे उपयोगकर्ता नाव आधीच वापरात आहे', 'error')
            return render_template('register.html')
        
        if User.query.filter_by(email=email).first():
            flash('हा ईमेल पत्ता आधीच वापरात आहे', 'error')
            return render_template('register.html')
        
        # Create new user
        user = User()
        user.username = username
        user.email = email
        user.password_hash = generate_password_hash(password)
        user.first_name = first_name
        user.last_name = last_name
        user.phone = phone
        
        # Generate STU ID
        user.generate_stu_id()
        
        db.session.add(user)
        db.session.commit()
        
        flash(f'नोंदणी यशस्वीरीत्या पूर्ण झाली! तुमचा STU ID: {user.stu_id}', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('तुम्ही यशस्वीरीत्या लॉग आउट झाला आहात', 'info')
    return redirect(url_for('login'))

@app.route('/student_dashboard')
@login_required
def student_dashboard():
    if current_user.is_admin:
        return redirect(url_for('admin_dashboard'))
    
    # Get form submission counts
    admission_count = AdmissionForm.query.filter_by(user_id=current_user.id).count()
    bonafide_count = BonafideRequest.query.filter_by(user_id=current_user.id).count()
    hostel_count = HostelApplication.query.filter_by(user_id=current_user.id).count()
    case_record_count = CaseRecord.query.filter_by(user_id=current_user.id).count()
    pratinidhan_count = PratinidhanForm.query.filter_by(user_id=current_user.id).count()
    
    return render_template('student_dashboard.html', 
                         admission_count=admission_count,
                         bonafide_count=bonafide_count,
                         hostel_count=hostel_count,
                         case_record_count=case_record_count,
                         pratinidhan_count=pratinidhan_count)

@app.route('/admin_dashboard')
@login_required
def admin_dashboard():
    if not current_user.is_admin:
        return redirect(url_for('student_dashboard'))
    
    # Get statistics
    total_students = User.query.filter_by(is_admin=False).count()
    total_admissions = AdmissionForm.query.count()
    total_bonafide = BonafideRequest.query.count()
    total_hostel = HostelApplication.query.count()
    total_case_records = CaseRecord.query.count()
    
    # Recent activity
    recent_students = User.query.filter_by(is_admin=False).order_by(User.created_at.desc()).limit(5).all()
    recent_admissions = AdmissionForm.query.order_by(AdmissionForm.created_at.desc()).limit(5).all()
    
    return render_template('admin_dashboard.html',
                         total_students=total_students,
                         total_admissions=total_admissions,
                         total_bonafide=total_bonafide,
                         total_hostel=total_hostel,
                         total_case_records=total_case_records,
                         recent_students=recent_students,
                         recent_admissions=recent_admissions)

# Form Routes
@app.route('/forms/admission', methods=['GET', 'POST'])
@login_required
def admission_form():
    if current_user.is_admin:
        return redirect(url_for('admin_dashboard'))
    
    if request.method == 'POST':
        # Handle file uploads
        student_photo = None
        parent_photo = None
        
        if 'student_photo' in request.files:
            file = request.files['student_photo']
            if file and allowed_file(file.filename):
                filename = secure_filename(f"{current_user.stu_id}_student_{file.filename}")
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                student_photo = filename
        
        if 'parent_photo' in request.files:
            file = request.files['parent_photo']
            if file and allowed_file(file.filename):
                filename = secure_filename(f"{current_user.stu_id}_parent_{file.filename}")
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                parent_photo = filename
        
        # Create admission form
        admission = AdmissionForm()
        admission.user_id = current_user.id
        admission.form_number = request.form.get('form_number')
        admission.school_name = request.form.get('school_name')
        admission.student_continuous_id = request.form.get('student_continuous_id')
        admission.udise_pen = request.form.get('udise_pen')
        admission.admission_class = request.form.get('admission_class')
        admission.birth_register_no = request.form.get('birth_register_no')
        admission.aadhar_no = request.form.get('aadhar_no')
        birth_date_str = request.form.get('birth_date')
        if birth_date_str:
            admission.birth_date = datetime.strptime(birth_date_str, '%Y-%m-%d').date()
        admission_date_str = request.form.get('admission_date')
        if admission_date_str:
            admission.admission_date = datetime.strptime(admission_date_str, '%Y-%m-%d').date()
        admission.gender = request.form.get('gender')
        admission.first_name_marathi = request.form.get('first_name_marathi')
        admission.last_name_marathi = request.form.get('last_name_marathi')
        admission.father_name = request.form.get('father_name')
        admission.mother_name = request.form.get('mother_name')
        admission.birth_date_words = request.form.get('birth_date_words')
        admission.religion = request.form.get('religion')
        admission.caste = request.form.get('caste')
        admission.subcaste = request.form.get('subcaste')
        admission.caste_certificate = request.form.get('caste_certificate')
        admission.is_minority = request.form.get('minority') == 'yes'
        admission.nationality = request.form.get('nationality')
        admission.mother_tongue = request.form.get('mother_tongue')
        admission.mobile_number = request.form.get('mobile_number')
        admission.bpl_status = request.form.get('bpl') == 'yes'
        admission.bpl_number = request.form.get('bpl_number')
        admission.disability_status = request.form.get('divyang') == 'yes'
        admission.disability_type = request.form.get('disability_type')
        admission.parent_full_name = request.form.get('parent_full_name')
        admission.address = request.form.get('address')
        admission.student_photo = student_photo
        admission.parent_photo = parent_photo
        
        db.session.add(admission)
        db.session.commit()
        
        flash('प्रवेश अर्ज यशस्वीरीत्या सबमिट केला गेला!', 'success')
        return redirect(url_for('student_dashboard'))
    
    return render_template('forms/admission_form.html')

@app.route('/forms/bonafide', methods=['GET', 'POST'])
@login_required
def bonafide_form():
    if current_user.is_admin:
        return redirect(url_for('admin_dashboard'))
    
    if request.method == 'POST':
        bonafide = BonafideRequest()
        bonafide.user_id = current_user.id
        bonafide.student_name = request.form.get('name')
        bonafide.academic_year = request.form.get('year')
        bonafide.standard = request.form.get('std')
        bonafide.division = request.form.get('div')
        bonafide.conduct = request.form.get('conduct')
        bonafide.caste = request.form.get('caste')
        dob_str = request.form.get('dob')
        if dob_str:
            bonafide.birth_date = datetime.strptime(dob_str, '%Y-%m-%d').date()
        bonafide.birth_place = request.form.get('birthplace')
        bonafide.place_of_issue = request.form.get('place')
        bonafide.student_id = request.form.get('id')
        
        db.session.add(bonafide)
        db.session.commit()
        
        flash('बोनाफाइड प्रमाणपत्राची विनंती सबमिट केली गेली!', 'success')
        return redirect(url_for('student_dashboard'))
    
    return render_template('forms/bonafide_form.html')

@app.route('/forms/hostel', methods=['GET', 'POST'])
@login_required
def hostel_form():
    if current_user.is_admin:
        return redirect(url_for('admin_dashboard'))
    
    if request.method == 'POST':
        # Handle file uploads
        parent_signature = None
        student_signature = None
        warden_signature = None
        
        for field_name in ['parent_signature', 'student_signature', 'warden_signature']:
            if field_name in request.files:
                file = request.files[field_name]
                if file and allowed_file(file.filename):
                    filename = secure_filename(f"{current_user.stu_id}_{field_name}_{file.filename}")
                    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    file.save(filepath)
                    if field_name == 'parent_signature':
                        parent_signature = filename
                    elif field_name == 'student_signature':
                        student_signature = filename
                    elif field_name == 'warden_signature':
                        warden_signature = filename
        
        hostel = HostelApplication()
        hostel.user_id = current_user.id
        hostel.hostel_name = request.form.get('hostel_name')
        hostel.hostel_address = request.form.get('address')
        hostel.parent_name = request.form.get('parent_name')
        hostel.parent_address = request.form.get('parent_address')
        hostel.student_name = request.form.get('student_name')
        hostel.student_address = request.form.get('student_address')
        hostel.phone = request.form.get('phone')
        hostel.caste = request.form.get('caste')
        hostel.birth_village = request.form.get('birth_village')
        hostel.birth_taluka = request.form.get('birth_taluka')
        hostel.birth_district = request.form.get('birth_district')
        dob_str = request.form.get('dob')
        if dob_str:
            hostel.birth_date = datetime.strptime(dob_str, '%Y-%m-%d').date()
        age_years_str = request.form.get('age_years')
        if age_years_str:
            hostel.age_years = int(age_years_str)
        age_months_str = request.form.get('age_months')
        if age_months_str:
            hostel.age_months = int(age_months_str)
        hostel.education = request.form.get('education')
        hostel.previous_school = request.form.get('previous_school')
        hostel.annual_income = request.form.get('annual_income')
        hostel.exam_results = request.form.get('exam_results')
        hostel.guardian_name = request.form.get('guardian_name')
        hostel.student_agreement_name = request.form.get('student_name_2')
        hostel.register_number = request.form.get('register_number')
        received_date_str = request.form.get('received_date')
        if received_date_str:
            hostel.received_date = datetime.strptime(received_date_str, '%Y-%m-%d').date()
        hostel.parent_signature = parent_signature
        hostel.student_signature = student_signature
        hostel.warden_signature = warden_signature
        
        db.session.add(hostel)
        db.session.commit()
        
        flash('वसतिगृह प्रवेश अर्ज यशस्वीरीत्या सबमिट केला गेला!', 'success')
        return redirect(url_for('student_dashboard'))
    
    return render_template('forms/hostel_form.html')

@app.route('/forms/case_record', methods=['GET', 'POST'])
@login_required
def case_record_form():
    if current_user.is_admin:
        return redirect(url_for('admin_dashboard'))
    
    if request.method == 'POST':
        case_record = CaseRecord()
        case_record.user_id = current_user.id
        case_record.name = request.form.get('name')
        dob_str = request.form.get('dob')
        if dob_str:
            case_record.birth_date = datetime.strptime(dob_str, '%Y-%m-%d').date()
        age_str = request.form.get('age')
        if age_str:
            case_record.age = int(age_str)
        case_record.gender = request.form.get('gender')
        case_record.education = request.form.get('education')
        case_record.father_name = request.form.get('father_name')
        case_record.father_education = request.form.get('father_education')
        case_record.father_occupation = request.form.get('father_occupation')
        case_record.father_income = request.form.get('father_income')
        case_record.mother_name = request.form.get('mother_name')
        case_record.mother_education = request.form.get('mother_education')
        case_record.mother_occupation = request.form.get('mother_occupation')
        case_record.mother_income = request.form.get('mother_income')
        case_record.guardian_name = request.form.get('guardian_name')
        case_record.guardian_education = request.form.get('guardian_education')
        case_record.guardian_occupation = request.form.get('guardian_occupation')
        case_record.guardian_income = request.form.get('guardian_income')
        case_record.guardian_address = request.form.get('guardian_address')
        case_record.guardian_mobile = request.form.get('guardian_mobile')
        case_record.relatives_address = request.form.get('relatives_address')
        case_record.permanent_address = request.form.get('permanent_address')
        case_record.economic_status = request.form.get('economic_status')
        case_record.area_type = request.form.get('area_type')
        case_record.religion = request.form.get('religion')
        case_record.caste = request.form.get('caste')
        case_record.mother_tongue = request.form.get('mother_tongue')
        case_record.info_relation_personal = request.form.get('info_relation_personal')
        case_record.contact_duration = request.form.get('contact_duration')
        case_record.info_trustworthiness = request.form.get('info_trustworthiness')
        case_record.info_completeness = request.form.get('info_completeness')
        case_record.complaint_details = request.form.get('complaint_details')
        case_record.past_treatment_medications = request.form.get('past_treatment_medications')
        case_record.past_treatment_professional = request.form.get('past_treatment_professional')
        case_record.past_treatment_physical = request.form.get('past_treatment_physical')
        case_record.past_treatment_other = request.form.get('past_treatment_other')
        
        db.session.add(case_record)
        db.session.commit()
        
        flash('केस रेकॉर्ड यशस्वीरीत्या सबमिट केला गेला!', 'success')
        return redirect(url_for('student_dashboard'))
    
    return render_template('forms/case_record_form.html')

@app.route('/forms/pratinidhan', methods=['GET', 'POST'])
@login_required
def pratinidhan_form():
    if current_user.is_admin:
        return redirect(url_for('admin_dashboard'))
    
    if request.method == 'POST':
        # Handle file uploads
        photo = None
        signature = None
        qualification_certificate = None
        experience_certificate = None
        
        for field_name in ['photo', 'signature', 'qualification_certificate', 'experience_certificate']:
            if field_name in request.files:
                file = request.files[field_name]
                if file and allowed_file(file.filename):
                    filename = secure_filename(f"{current_user.stu_id}_{field_name}_{file.filename}")
                    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    file.save(filepath)
                    if field_name == 'photo':
                        photo = filename
                    elif field_name == 'signature':
                        signature = filename
                    elif field_name == 'qualification_certificate':
                        qualification_certificate = filename
                    elif field_name == 'experience_certificate':
                        experience_certificate = filename
        
        pratinidhan = PratinidhanForm()
        pratinidhan.user_id = current_user.id
        pratinidhan.application_number = request.form.get('application_number')
        app_date_str = request.form.get('application_date')
        if app_date_str:
            pratinidhan.application_date = datetime.strptime(app_date_str, '%Y-%m-%d').date()
        pratinidhan.applicant_name = request.form.get('applicant_name')
        pratinidhan.father_name = request.form.get('father_name')
        birth_date_str = request.form.get('birth_date')
        if birth_date_str:
            pratinidhan.birth_date = datetime.strptime(birth_date_str, '%Y-%m-%d').date()
        pratinidhan.birth_place = request.form.get('birth_place')
        pratinidhan.permanent_address = request.form.get('permanent_address')
        pratinidhan.current_address = request.form.get('current_address')
        pratinidhan.mobile_number = request.form.get('mobile_number')
        pratinidhan.email = request.form.get('email')
        pratinidhan.qualification = request.form.get('qualification')
        pratinidhan.institution_name = request.form.get('institution_name')
        pratinidhan.passing_year = request.form.get('passing_year')
        pratinidhan.marks_percentage = request.form.get('marks_percentage')
        pratinidhan.representation_type = request.form.get('representation_type')
        pratinidhan.organization_name = request.form.get('organization_name')
        pratinidhan.designation = request.form.get('designation')
        pratinidhan.duration = request.form.get('duration')
        pratinidhan.photo = photo
        pratinidhan.signature = signature
        pratinidhan.qualification_certificate = qualification_certificate
        pratinidhan.experience_certificate = experience_certificate
        
        db.session.add(pratinidhan)
        db.session.commit()
        
        flash('प्रतिनिधान प्रमाण पत्र अर्ज यशस्वीरीत्या सबमिट केला गेला!', 'success')
        return redirect(url_for('student_dashboard'))
    
    return render_template('forms/pratinidhan_form.html')

# Certificate generation
@app.route('/certificate/<int:bonafide_id>')
@login_required
def generate_certificate(bonafide_id):
    bonafide = BonafideRequest.query.get_or_404(bonafide_id)
    
    # Check if user owns this request or is admin
    if not current_user.is_admin and bonafide.user_id != current_user.id:
        flash('तुम्हाला या प्रमाणपत्राचा अधिकार नाही', 'error')
        return redirect(url_for('student_dashboard'))
    
    return render_template('forms/bonafide_certificate.html', bonafide=bonafide)

# Admin routes
@app.route('/admin/students')
@login_required
def admin_students():
    if not current_user.is_admin:
        return redirect(url_for('student_dashboard'))
    
    students = User.query.filter_by(is_admin=False).order_by(User.stu_id).all()
    return render_template('admin/student_management.html', students=students)

@app.route('/admin/forms')
@login_required
def admin_forms():
    if not current_user.is_admin:
        return redirect(url_for('student_dashboard'))
    
    admissions = AdmissionForm.query.order_by(AdmissionForm.created_at.desc()).all()
    bonafides = BonafideRequest.query.order_by(BonafideRequest.created_at.desc()).all()
    hostels = HostelApplication.query.order_by(HostelApplication.created_at.desc()).all()
    case_records = CaseRecord.query.order_by(CaseRecord.created_at.desc()).all()
    pratinidhan_forms = PratinidhanForm.query.order_by(PratinidhanForm.created_at.desc()).all()
    
    return render_template('admin/form_submissions.html',
                         admissions=admissions,
                         bonafides=bonafides,
                         hostels=hostels,
                         case_records=case_records,
                         pratinidhan_forms=pratinidhan_forms)

# API endpoints
@app.route('/api/check_stu_id/<stu_id>')
@login_required
def check_stu_id(stu_id):
    """Check if STU ID is available"""
    user = User.query.filter_by(stu_id=stu_id).first()
    return jsonify({'available': user is None})

@app.route('/api/update_form_status', methods=['POST'])
@login_required
def update_form_status():
    if not current_user.is_admin:
        return jsonify({'error': 'Unauthorized'}), 403
    
    json_data = request.get_json()
    if not json_data:
        return jsonify({'error': 'No JSON data provided'}), 400
    
    form_type = json_data.get('form_type')
    form_id = json_data.get('form_id')
    status = json_data.get('status')
    
    model_map = {
        'admission': AdmissionForm,
        'bonafide': BonafideRequest,
        'hostel': HostelApplication,
        'case_record': CaseRecord,
        'pratinidhan': PratinidhanForm
    }
    
    if form_type not in model_map:
        return jsonify({'error': 'Invalid form type'}), 400
    
    form_obj = model_map[form_type].query.get(form_id)
    if not form_obj:
        return jsonify({'error': 'Form not found'}), 404
    
    form_obj.status = status
    db.session.commit()
    
    return jsonify({'success': True})

@app.route('/uploads/<filename>')
@login_required
def uploaded_file(filename):
    """Serve uploaded files"""
    return send_file(os.path.join(app.config['UPLOAD_FOLDER'], filename))
