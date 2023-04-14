from flask import Flask, render_template, request, flash, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import sql
from werkzeug.utils import secure_filename
import os
from builtins import str
app = Flask(__name__)
app.secret_key = 'wazireducationsocity'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/wes_admission_details'
db = SQLAlchemy(app)

app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['ALLOWED_EXTENSIONS'] = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower(
           ) in app.config['ALLOWED_EXTENSIONS']


# Create the uploads folder if it doesn't exist
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])


class Registration_from(db.Model):
    __tablename__ = 'registration_from'
    sno = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    father_name = db.Column(db.String(100), nullable=False)
    mother_name = db.Column(db.String(100), nullable=False)
    class_name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    mobile = db.Column(db.String(12), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(10), nullable=False)

    def __int__(self):
        return self.sno


class Admission_from(db.Model):
    __tablename__ = 'admission_from'
    s_id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    r_id = db.Column(db.Integer, db.ForeignKey('registration_from.sno'))

    know_about_wes = db.Column(db.String(50), nullable=False)

  # Why do you want to join WES over other institutes?
    why_join_wes = db.Column(db.Text, nullable=False)

    # Color Passport Photograph
    photo = db.Column(db.String(255))

    # Name of the student
    first_name = db.Column(db.String(50), nullable=False)
    middle_name = db.Column(db.String(50), nullable=True)
    last_name = db.Column(db.String(50), nullable=False)
    student_mob_no = db.Column(db.BigInteger, nullable=False)
    student_email = db.Column(db.String(100), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    gender = db.Column(db.String(10), nullable=False)

 # Name of the Parent/Guardian/Father
    father_first_name = db.Column(db.String(50), nullable=False)
    father_middle_name = db.Column(db.String(50), nullable=True)
    father_last_name = db.Column(db.String(50), nullable=False)
    father_profession = db.Column(db.String(50), nullable=False)
    father_mob_no = db.Column(db.BigInteger, nullable=False)
    father_email = db.Column(db.String(100), nullable=False)

 # Name of the Parent/Guardian/Mother
    mother_first_name = db.Column(db.String(50), nullable=False)
    mother_middle_name = db.Column(db.String(50), nullable=True)
    mother_last_name = db.Column(db.String(50), nullable=False)
    mother_profession = db.Column(db.String(50), nullable=False)
    mother_mob_no = db.Column(db.BigInteger, nullable=False)
    mother_email = db.Column(db.String(100), nullable=False)

 # Name of the Parent/Guardian
    guardian_first_name = db.Column(db.String(50), nullable=False)
    guardian_middle_name = db.Column(db.String(50), nullable=True)
    guardian_last_name = db.Column(db.String(50), nullable=False)
    guardian_profession = db.Column(db.String(50), nullable=False)
    guardian_mob_no = db.Column(db.BigInteger, nullable=False)
    guardian_email = db.Column(db.String(100), nullable=False)

  # Address for correspondence
    correspondence_address = db.Column(db.Text, nullable=False)
    correspondence_city = db.Column(db.String(50), nullable=False)
    correspondence_state = db.Column(db.String(50), nullable=False)
    correspondence_pin_code = db.Column(db.Integer, nullable=False)

    # Permanent Address
    permanent_address = db.Column(db.Text, nullable=False)
    permanent_city = db.Column(db.String(50), nullable=False)
    permanent_state = db.Column(db.String(50), nullable=False)
    permanent_pin_code = db.Column(db.Integer, nullable=False)

    # Latest/Ongoing Education
    latest_ongoing = db.Column(db.String(100), nullable=False)
    school_name = db.Column(db.String(100), nullable=False)
    class_batch = db.Column(db.String(50), nullable=False)
    start_year = db.Column(db.Integer, nullable=False)

    # Enclosures
    enclosures = db.Column(db.String(250))

   # Name of the student
    student_place = db.Column(db.String(50), nullable=False)
    student_date = db.Column(db.Date, nullable=False)
    student_signature = db.Column(db.String(255))

   # Name of the Parent/ guardian
    parent_place = db.Column(db.String(50), nullable=False)
    parent_date = db.Column(db.Date, nullable=False)
    guardian_signature = db.Column(db.String(255))

 # For Office Use Only :
    form_number = db.Column(db.Integer)
    date = db.Column(db.Date)
    reg_number = db.Column(db.Integer)
    course = db.Column(db.String(100))
    batch = db.Column(db.String(100))
    start_date = db.Column(db.Date)

    def __int__(self):
        return self.r_id


@app.route("/")
def page():
    return render_template('dashboard.html')


@app.route("/registration", methods=['GET', 'POST'])
def registration():
    if request.method == 'POST':

        name = request.form.get('name')
        father_name = request.form.get('F_name')
        mother_name = request.form.get('M_name')
        class_name = request.form.get("class")
        email = request.form.get('eml')
        phone = request.form.get('mbl')
        age = int(request.form.get('dob'))
        gender = request.form.get('gender')

        save_reg = Registration_from(name=name, father_name=father_name, mother_name=mother_name, class_name=class_name,
                                     email=email, mobile=phone,
                                     age=age, gender=gender)
        db.session.add(save_reg)
        db.session.commit()

        Reg_id = save_reg.sno
        registration_data = Registration_from.query.filter_by(
            sno=Reg_id).first()

        flash("Your form submitted Successfully.")
        if ((age >= 7) and (age <= 12)):
            return render_template('test1.html', registration_data=registration_data)
        elif ((age > 12) and (age <= 18)):
            return render_template('test2.html', registration_data=registration_data)
        elif ((age > 18) and (age <= 22)):
            return render_template('test3.html', registration_data=registration_data)
    else:
        return render_template('form_page.html')


@app.route("/register_student")
def register_student():
    registration_form = Registration_from.query.all()
    return render_template('reg_list.html', registration_form=registration_form)


class Marks(db.Model):
    __tablename__ = 'marks'
    m_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    mr_id = db.Column(db.Integer, db.ForeignKey('registration_from.sno'))
    hindi = db.Column(db.String(255))
    english = db.Column(db.String(255))
    math = db.Column(db.String(255))
    total = db.Column(db.String(255))
    ans_sheet = db.Column(db.String(255))

    def __int__(self):
        return self.m_id


with app.app_context():
    # create_table
    db.create_all()


@app.route('/marks_form/<int:sno>', methods=['GET', 'POST'])
def marks_form(sno):
    if request.method == 'POST':

        Hindi = request.form.get('hindi')
        English = request.form.get('english')
        Math = request.form.get('math')
        Total = request.form.get('total')
        Ans_sheet = request.files.get('ans_key')

        masrks_save = Marks(mr_id=sno, hindi=Hindi, english=English,
                            math=Math, total=Total, ans_sheet=Ans_sheet.filename)
        db.session.add(masrks_save)
        db.session.commit()

        return redirect(url_for('register_student'))
    else:
        return render_template('marks_form.html')


@app.route("/admission/<int:r_id>", methods=['GET', 'POST'])
def admission(r_id):
    if request.method == 'POST':

        Know_about = request.form.get('about_WES')
        reasons = request.form.get('joining_reasons')
        Photo = request.files.get('Photo')

        # Personal Information Section
        fname = request.form.get('first-name')
        mname = request.form.get('middle-name')
        lname = request.form.get('last-name')
        email = request.form.get('eml')
        mobile = request.form.get('mbl')
        DOB = request.form.get('dob')
        Gender = request.form.get('gender')

        # Name of the Parent/Guardian/Father
        Father_fname = request.form.get('F_fname')
        Father_mname = request.form.get('F_mname')
        Father_lname = request.form.get('F_lname')
        Father_pfn = request.form.get('F_pfn')
        Father_mail = request.form.get('F_mail')
        Father_num = request.form.get('F_num')

        # Name of the Parent/Guardian/Mother
        Mother_fname = request.form.get('M_fname')
        Mother_mname = request.form.get('M_mname')
        Mother_lname = request.form.get('M_lname')
        Mother_pfn = request.form.get('M_pfn')
        Mother_mail = request.form.get('M_mail')
        Mother_num = request.form.get('M_num')

        # Name of the Parent/Guardian/Mother
        Guardian_fname = request.form.get('G_fname')
        Guardian_mname = request.form.get('G_mname')
        Guardian_lname = request.form.get('G_lname')
        Guardian_pfn = request.form.get('G_pfn')
        Guardian_mail = request.form.get('G_mail')
        Guardian_num = request.form.get('G_num')

        # Address for correspondence
        Cor_add = request.form.get('C_add')
        Cor_city = request.form.get('C_city')
        Cor_state = request.form.get('C_state')
        Cor_zip = request.form.get('C_zip')

        # Permanent Address
        Per_add = request.form.get('P_add')
        Per_city = request.form.get('P_city')
        Per_state = request.form.get('P_state')
        Per_zip = request.form.get('P_zip')

        # Latest/Ongoing Education
        Edu_type = request.form.get('education-type')
        Sch_name = request.form.get('school-name')
        Class_batch = request.form.get('class-batch')
        Start_year = request.form.get('start-year')

        # Enclosures
        Enclosure = ','.join(request.form.getlist('enclosures'))

        # Some Extra details of Student
        Stu_place = request.form.get('S_place')
        Stu_date = request.form.get('S_date')
        Stu_sign = request.files.get('S_sign')
        # Stu_sign.save(os.path.join(student_folder))

        # Some Extra details of Parent/ guardian
        Par_place = request.form.get('P_place')
        Par_date = request.form.get('P_date')
        Par_sign = request.files.get('P_sign')
        # Par_sign.save(os.path.join(student_folder))

        # For Office Use Only :
        Form_No = request.form.get('form_no')
        Date = request.form.get('dt')
        Reg_No = request.form.get('reg_no')
        Course = request.form.get('course')
        Batch = request.form.get('batch')
        Start_date = request.form.get('start_dt')

        # To query Registration form and filter data by name, Mobile no. and email
        # r_id = Registration_from.query.filter(sql.and_(Registration_from.mobile == mobile,

        save_adm = Admission_from(r_id=r_id, know_about_wes=Know_about, why_join_wes=reasons, photo=Photo.filename, first_name=fname, middle_name=mname, last_name=lname, student_mob_no=mobile, student_email=email, date_of_birth=DOB, gender=Gender, father_first_name=Father_fname, father_middle_name=Father_mname,
                                  father_last_name=Father_lname, father_profession=Father_pfn, father_mob_no=Father_num, father_email=Father_mail, mother_first_name=Mother_fname, mother_middle_name=Mother_mname, mother_last_name=Mother_lname, mother_profession=Mother_pfn, mother_mob_no=Mother_num, mother_email=Mother_mail, guardian_first_name=Guardian_fname, guardian_middle_name=Guardian_mname, guardian_last_name=Guardian_lname, guardian_profession=Guardian_pfn, guardian_mob_no=Guardian_num, guardian_email=Guardian_mail, correspondence_address=Cor_add, correspondence_city=Cor_city, correspondence_state=Cor_state, correspondence_pin_code=Cor_zip, permanent_address=Per_add, permanent_city=Per_city, permanent_state=Per_state, permanent_pin_code=Per_zip, latest_ongoing=Edu_type, school_name=Sch_name, class_batch=Class_batch, start_year=Start_year, enclosures=Enclosure, student_place=Stu_place, student_date=Stu_date, student_signature=Stu_sign.filename, parent_place=Par_place, parent_date=Par_date, guardian_signature=Par_sign.filename, form_number=Form_No, date=Date, reg_number=Reg_No, course=Course, batch=Batch, start_date=Start_date)

        db.session.add(save_adm)
        db.session.commit()

        # create a folder name r_id
        student_id = r_id
        # print(student_id)
        student_folder = os.path.join(
            app.config['UPLOAD_FOLDER'], str(student_id))
        if not os.path.exists(student_folder):
            os.makedirs(student_folder)

        if Photo:
            filename = secure_filename(Photo.filename)
            if Photo and allowed_file(Photo.filename):
                filename = secure_filename(Photo.filename)
                Photo.save(os.path.join(student_folder, filename))
        if Stu_sign:
            filename = secure_filename(Stu_sign.filename)
            if Stu_sign and allowed_file(Stu_sign.filename):
                filename = secure_filename(Stu_sign.filename)
                Stu_sign.save(os.path.join(student_folder, filename))
        if Par_sign:
            filename = secure_filename(Par_sign.filename)
            if Par_sign and allowed_file(Par_sign.filename):
                filename = secure_filename(Par_sign.filename)
                Par_sign.save(os.path.join(student_folder, filename))

        flash("Submitted Successfully.")
        return redirect(url_for('student_list'))
    else:
        return render_template('admission_form.html')


@app.route("/student_list")
def student_list():
    admission_form = Admission_from.query.all()
    return render_template('adm_student.html', admission_form=admission_form)


@app.route('/student_details/<int:s_id>')
def student_details(s_id):
    student = Admission_from.query.get(s_id)
    if student is None:
        return 'Student not found'
    photo_url = url_for('static', filename='uploads/' +
                        str(student.r_id) + "/" + student.photo)
    stu_sign_url = url_for('static', filename='uploads/' +
                           str(student.r_id) + "/" + student.student_signature)
    par_sign_url = url_for('static', filename='uploads/' +
                           str(student.r_id) + "/" + student.guardian_signature)
    # print(stu_sign_url)
    return render_template('student_details.html', student=student, photo_url=photo_url, stu_sign_url=stu_sign_url, par_sign_url=par_sign_url)


@app.route('/edit_students/<int:s_id>', methods=['GET', 'POST'])
def edit_students(s_id):
    student = Admission_from.query.get(s_id)
    if request.method == 'POST':

        student.know_about_wes = request.form['about_WES']
        student.why_join_wes = request.form['joining_reasons']

        # Personal Information Section
        student.first_name = request.form['first-name']
        student.middle_name = request.form['middle-name']
        student.last_name = request.form['last-name']
        student.student_email = request.form['eml']
        student.student_mob_no = request.form['mbl']
        student.date_of_birth = request.form['dob']
        student.gender = request.form['gender']

        # Name of the Parent/Guardian/Father
        student.father_first_name = request.form['F_fname']
        student.father_middle_name = request.form['F_mname']
        student.father_last_name = request.form['F_lname']
        student.father_profession = request.form['F_pfn']
        student.father_email = request.form['F_mail']
        student.father_mob_no = request.form['F_num']

        # Name of the Parent/Guardian/Mother
        student.mother_first_name = request.form['M_fname']
        student.mother_middle_name = request.form['M_mname']
        student.mother_last_name = request.form['M_lname']
        student.mother_profession = request.form['M_pfn']
        student.mother_email = request.form['M_mail']
        student.mother_mob_no = request.form['M_num']

        # Name of the Parent/Guardian/Mother
        student.guardian_first_name = request.form['G_fname']
        student.guardian_middle_name = request.form['G_mname']
        student.guardian_last_name = request.form['G_lname']
        student.guardian_profession = request.form['G_pfn']
        student.guardian_email = request.form['G_mail']
        student.guardian_mob_no = request.form['G_num']

        # Address for correspondence
        student.correspondence_address = request.form['C_add']
        student.correspondence_city = request.form['C_city']
        student.correspondence_state = request.form['C_state']
        student.correspondence_pin_code = request.form['C_zip']

        # Permanent Address
        student.permanent_address = request.form['P_add']
        student.permanent_city = request.form['P_city']
        student.permanent_state = request.form['P_state']
        student.permanent_pin_code = request.form['P_zip']

        # Latest/Ongoing Education
        student.latest_ongoing = request.form['education-type']
        student.school_name = request.form['school-name']
        student.class_batch = request.form['class-batch']
        student.start_year = request.form['start-year']

        # Enclosures
        # Enclosure = ','.join(request.form['enclosures'])

        # Some Extra details of Student
        student.student_place = request.form['S_place']
        student.student_date = request.form['S_date']

        # Some Extra details of Parent/ guardian
        student.parent_place = request.form['P_place']
        student.parent_date = request.form['P_date']

        # For Office Use Only :
        student.form_number = request.form['form_no']
        student.date = request.form['dt']
        student.reg_number = request.form['reg_no']
        student.course = request.form['course']
        student.batch = request.form['batch']
        student.start_date = request.form['start_dt']

        db.session.commit()

        return redirect(url_for('student_list'))
    else:

        photo_url = url_for('static', filename='uploads/' +
                            str(student.r_id) + "/" + student.photo)
        stu_sign_url = url_for('static', filename='uploads/' +
                               str(student.r_id) + "/" + student.student_signature)
        par_sign_url = url_for('static', filename='uploads/' +
                               str(student.r_id) + "/" + student.guardian_signature)
        return render_template('edit_students.html', student=student, photo_url=photo_url, stu_sign_url=stu_sign_url, par_sign_url=par_sign_url)


app.run(debug=True)
