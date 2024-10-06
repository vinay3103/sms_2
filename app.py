from flask import Flask, jsonify, render_template, request, redirect, url_for, flash, send_from_directory
from werkzeug.utils import secure_filename
import os
import secrets


app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Required for flashing messages
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_PATH'] = 16 * 1024 * 1024  # Max upload size 16MB

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Dummy student data (replace with actual data from your Python file)
students = {
    "21bce8331": {"id": "21bce8331", "password": "1234", "name": "vinay"},
    "21bce8938": {"id": "21bce8938", "password": "12345", "name": "teja"},
    "21bce8939": {"id": "21bce8939", "password": "123456", "name": "rishitha"},
    "21bce8000": {"id": "21bce8000", "password": "1234567", "name": "trupthi"},
    "21bce8103": {"id": "21bce8103", "password": "12345678", "name": "vishnu"},
    "21bce8234": {"id": "21bce8234", "password": "123456789", "name": "shubham"}
}

attendence_data = {
    "21bce8331": {
        "Maths": {"day 1": "Present", "day 2": "Absent"},
        "Science": {"day 1": "Absent", "day 2": "Present"},
        "English": {"day 1": "Present", "day 2": "Present"}
    },
    "21bce8938": {
        "Maths": {"day 1": "Present", "day 2": "Absent"},
        "Science": {"day 1": "Present", "day 2": "Present"},
        "English": {"day 1": "Present", "day 2": "Present"}
    },
    "21bce8939": {
        "Maths": {"day 1": "Present", "day 2": "Present"},
        "Science": {"day 1": "Absent", "day 2": "Present"},
        "English": {"day 1": "Present", "day 2": "Present"}
    },
    "21bce8000": {
        "Maths": {"day 1": "Present", "day 2": "Absent"},
        "Science": {"day 1": "Absent", "day 2": "Present"},
        "English": {"day 1": "Present", "day 2": "Present"}
    },
    "21bce8103": {
        "Maths": {"day 1": "Present", "day 2": "Absent"},
        "Science": {"day 1": "Present", "day 2": "Present"},
        "English": {"day 1": "Present", "day 2": "Present"}
    },
    "21bce8234": {
        "Maths": {"day 1": "Present", "day 2": "Absent"},
        "Science": {"day 1": "Present", "day 2": "Present"},
        "English": {"day 1": "Present", "day 2": "Present"}
    }
}

marks_data = {
    "21bce8331": {
        "Maths": {"Assignment 1": "85", "Quiz 1": "90"},
        "Science": {"Assignment 1": "90", "Quiz 1": "95"},
        "English": {"Assignment 1": "100", "Quiz 1": "95"}
    },
    "21bce8938": {
        "Maths": {"Assignment 1": "85", "Quiz 1": "90"},
        "Science": {"Assignment 1": "90", "Quiz 1": "95"},
        "English": {"Assignment 1": "100", "Quiz 1": "95"}
    },
    "21bce8939": {
        "Maths": {"Assignment 1": "85", "Quiz 1": "90"},
        "Science": {"Assignment 1": "90", "Quiz 1": "95"},
        "English": {"Assignment 1": "100", "Quiz 1": "95"}
    },
    "21bce8000": {
        "Maths": {"Assignment 1": "85", "Quiz 1": "90"},
        "Science": {"Assignment 1": "90", "Quiz 1": "95"},
        "English": {"Assignment 1": "100", "Quiz 1": "95"}
    },
    "21bce8103": {
        "Maths": {"Assignment 1": "85", "Quiz 1": "90"},
        "Science": {"Assignment 1": "90", "Quiz 1": "95"},
        "English": {"Assignment 1": "100", "Quiz 1": "95"}
    },
    "21bce8234": {
        "Maths": {"Assignment 1": "85", "Quiz 1": "90"},
        "Science": {"Assignment 1": "90", "Quiz 1": "95"},
        "English": {"Assignment 1": "100", "Quiz 1": "95"}
    }
}

faculty = {
    "faculty1": {"id": "faculty1", "password": "faculty123", "name": "Dr. Smith", "subjects": "Maths"},
    "faculty2": {"id": "faculty2", "password": "faculty456", "name": "Prof. Johnson", "subjects": "Science"},
    "faculty3": {"id": "faculty3", "password": "faculty789", "name": "Prof. Sampath", "subjects": "English"}
}
assignments={}

@app.route('/student_login', methods=['POST'])
def student_login():
    student_id = request.form['student_id']
    password = request.form['password']
    
    student = students.get(student_id)
    if student and student['password'] == password:
        return redirect(url_for('student_portal', student_id=student_id))
    return redirect(url_for('login', error='Invalid credentials'))

@app.route('/developers')
def developers():
    return render_template('developers.html')

@app.route('/faculty_portal/<string:faculty_id>')
def faculty_portal(faculty_id):
    faculty_member = faculty.get(faculty_id)
    if not faculty_member:
        return "Faculty not found", 404
    return render_template('faculty_portal.html', faculty_id=faculty_id, faculty=faculty_member)
@app.route('/add_marks/<string:faculty_id>', methods=['GET', 'POST'])
def add_marks(faculty_id):
    if request.method == 'POST':
        subject = faculty[faculty_id]['subjects']
        
        for key, value in request.form.items():
            if key.startswith('marks_'):
                student_id = key.split('_')[1]
                marks = int(value)
                
                if 1 <= marks <= 100:
                    if student_id in marks_data:
                        if subject in marks_data[student_id]:
                            marks_data[student_id][subject][request.form['assignment_type']] = marks
                        else:
                            marks_data[student_id][subject] = {request.form['assignment_type']: marks}
                    else:
                        marks_data[student_id] = {subject: {request.form['assignment_type']: marks}}
                else:
                    flash(f"Marks for student {student_id} should be between 1 and 100", "error")
                    return redirect(url_for('error', error="Marks should be between 1 and 100"))
        
        return redirect(url_for('faculty_portal', faculty_id=faculty_id))
    
    students = get_all_students()  # Fetch all students
    return render_template('add_marks.html', faculty_id=faculty_id, students=students)

def get_all_students():
    return students.values()

@app.route('/add_attendance/<string:faculty_id>', methods=['GET', 'POST'])
def add_attendance(faculty_id):
    if request.method == 'POST':
        day = request.form['day']
        subject = faculty[faculty_id]['subjects']
        
        for key, value in request.form.items():
            if key.startswith('attendance_'):
                student_id = key.split('_')[1]
                attendance = value
                
                if student_id in attendence_data:
                    if subject in attendence_data[student_id]:
                        attendence_data[student_id][subject][day] = attendance
                    else:
                        attendence_data[student_id][subject] = {day: attendance}
                else:
                    attendence_data[student_id] = {subject: {day: attendance}}

        return redirect(url_for('faculty_portal', faculty_id=faculty_id))
    
    students = get_all_students()  # Fetch all students
    return render_template('add_attendance.html', faculty_id=faculty_id, students=students)

@app.route('/faculty_login', methods=['GET', 'POST'])
def faculty_login():
    if request.method == 'POST':
        faculty_id = request.form['faculty_id']
        return redirect(url_for('faculty_portal', faculty_id=faculty_id))
    return render_template('login.html')

@app.route('/student_portal/<student_id>')
def student_portal(student_id):
    student = students.get(student_id)  # Assuming `students` is your data dictionary
    if student:
        return render_template('student_portal.html', student=student)
    else:
        return "Student not found", 404
    
@app.route('/marks-page/<student_id>')
def marks_page(student_id):
    student = students.get(student_id)
    if student:
        marks = marks_data.get(student_id)  # Fetch marks for the student
        return render_template('marks-page.html', student=student, marks=marks)
    else:
        return "Student not found", 404

@app.route('/attendence-page/<student_id>')
def attendence_page(student_id):
    student = students.get(student_id)
    if student:
        attendence = attendence_data.get(student_id)  # Fetch attendance for the student
        return render_template('attendence-page.html', student=student, attendence=attendence)
    else:
        return "Student not found", 404

@app.route('/logout')
def logout():
    # Logic to log out the user
    return redirect(url_for('login'))

@app.route('/success')
def success():
    return render_template('success.html')

@app.route('/error')
def error():
    error_message = request.args.get('error')
    return render_template('error.html', error=error_message)

@app.route('/success2')
def success2():
    return render_template('success2.html')

@app.route('/error2')
def error2():
    error_message = request.args.get('error')
    return render_template('error2.html', error=error_message)

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_type = request.form['user_type']
        user_id = request.form['user_id']
        password = request.form['password']
        
        if user_type == 'faculty':
            faculty_member = faculty.get(user_id)
            if faculty_member and faculty_member['password'] == password:
                return redirect(url_for('faculty_portal', faculty_id=user_id))
            else:
                return "Invalid faculty credentials", 401
        
        elif user_type == 'student':
            student = students.get(user_id)
            if student and student['password'] == password:
                return redirect(url_for('student_portal', student_id=user_id))
            else:
                return "Invalid student credentials", 401
        
    return render_template('login.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'pdf', 'docx', 'txt', 'jpg', 'png'}

@app.route('/upload_assignment/<student_id>', methods=['GET', 'POST'])
def upload_assignment(student_id):
    if request.method == 'POST':
        subject = request.form['subject']
        if 'file' not in request.files:
            flash('No file part')
            print("No file part")
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            print("No selected file")
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            if student_id not in assignments:
                assignments[student_id] = []
            assignments[student_id].append({'filename': filename, 'filepath': filepath, 'subject': subject})
            print(f"File uploaded: {filename} to {filepath}")
            print(f"Updated assignments: {assignments}")
            return redirect(url_for('student_portal', student_id=student_id))
    print(f"Rendering upload page for {student_id}")
    return render_template('upload_assignment.html', student_id=student_id)

@app.route('/view_assignments/<faculty_id>',methods=['GET'])
def view_assignments(faculty_id):
    return render_template('view_assignments.html', faculty_id=faculty_id, assignments=assignments)

@app.route('/download/<path:filename>')
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/grade_assignment/<student_id>/<filename>', methods=['GET', 'POST'])
def grade_assignment(student_id, filename):
    if request.method == 'POST':
        grade = request.form['grade']
        try:
            grade = int(grade)
            if 1 <= grade <= 100:
                # Update the assignments data
                assignment_found = False
                for assignment in assignments.get(student_id, []):
                    if assignment['filename'] == filename:
                        assignment['grade'] = grade
                        assignment_found = True
                        break
                
                if assignment_found:
                    # Update marks_data to reflect the new grade
                    subject = next((a['subject'] for a in assignments.get(student_id, []) if a['filename'] == filename), None)
                    if subject:
                        if student_id not in marks_data:
                            marks_data[student_id] = {}
                        if subject not in marks_data[student_id]:
                            marks_data[student_id][subject] = {}
                        # Assuming all assignments have a name and we update that
                        marks_data[student_id][subject][filename] = grade
                
                flash('Grade successfully updated.', 'success')
            else:
                flash('Grade must be between 1 and 100.', 'error')
        except ValueError:
            flash('Invalid grade input. Please enter a number.', 'error')
        
        return redirect(url_for('view_assignments', faculty_id='faculty1'))

    assignment = next((a for a in assignments.get(student_id, []) if a['filename'] == filename), None)
    if assignment is None:
        return "Assignment not found", 404

    return render_template('grade_assignment.html', student_id=student_id, assignment=assignment,filename=filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000,debug=True)
