import os
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

# Get the base directory of the project
basedir = os.path.abspath(os.path.dirname(__file__))

# Initialize the Flask application
app = Flask(__name__)
# Configure the secret key for session management (used for flash messages)
app.config['SECRET_KEY'] = 'a-very-secret-key-that-should-be-changed'
import os
database_url = os.environ.get('DATABASE_URL', 'sqlite:///students.db')
app.config['SQLALCHEMY_DATABASE_URI'] = database_url.replace("postgres://", "postgresql://", 1)
# Disable SQLAlchemy's event system to save resources, as it's not needed here
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the SQLAlchemy object with the Flask app
db = SQLAlchemy(app)

# --- Database Models ---

class Student(db.Model):
    """
    Represents a student in the database.
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    roll_number = db.Column(db.Integer, unique=True, nullable=False)
    # Establish a one-to-many relationship with the Grade model.
    # 'backref' creates a 'student' attribute on the Grade model to access the parent Student.
    # 'cascade' ensures that when a student is deleted, all their associated grades are also deleted.
    grades = db.relationship('Grade', backref='student', cascade='all, delete-orphan')

    def calculate_average(self):
        """Calculates the average grade for the student."""
        if not self.grades:
            return 0.0
        total_score = sum(grade.score for grade in self.grades)
        return round(total_score / len(self.grades), 2)

    def __repr__(self):
        """String representation of the Student object."""
        return f'<Student {self.name} ({self.roll_number})>'

class Grade(db.Model):
    """
    Represents a grade for a specific subject for a student.
    """
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(100), nullable=False)
    score = db.Column(db.Float, nullable=False)
    # Foreign key to link this grade to a specific student.
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)

    def __repr__(self):
        """String representation of the Grade object."""
        return f'<Grade {self.subject}: {self.score}>'


# --- Flask Routes ---

@app.route('/')
def index():
    """
    Main page that displays all students and their details.
    """
    students = Student.query.all()
    # Calculate additional info for display
    student_data = []
    for student in students:
        student_data.append({
            'id': student.id,
            'name': student.name,
            'roll_number': student.roll_number,
            'grades': student.grades,
            'average': student.calculate_average()
        })
    return render_template('index.html', students=student_data)

@app.route('/add_student', methods=['POST'])
def add_student():
    """
    Handles the form submission for adding a new student.
    """
    name = request.form.get('name')
    roll_number = request.form.get('roll_number')

    if not name or not roll_number:
        flash('Name and Roll Number are required.', 'error')
        return redirect(url_for('index'))

    try:
        roll_number = int(roll_number)
    except ValueError:
        flash('Roll Number must be an integer.', 'error')
        return redirect(url_for('index'))

    # Check if a student with the same roll number already exists
    existing_student = Student.query.filter_by(roll_number=roll_number).first()
    if existing_student:
        flash('A student with this roll number already exists.', 'error')
        return redirect(url_for('index'))

    new_student = Student(name=name, roll_number=roll_number)
    db.session.add(new_student)
    db.session.commit()
    flash(f'Student "{name}" added successfully!', 'success')
    return redirect(url_for('index'))


@app.route('/add_grade/<int:student_id>', methods=['POST'])
def add_grade(student_id):
    """
    Handles the form submission for adding a grade to a student.
    """
    student = Student.query.get_or_404(student_id)
    subject = request.form.get('subject')
    score_str = request.form.get('score')

    if not subject or not score_str:
        flash('Subject and Score are required.', 'error')
        return redirect(url_for('index'))

    try:
        score = float(score_str)
        if not (0 <= score <= 100):
            raise ValueError("Score out of range.")
    except ValueError:
        flash('Score must be a number between 0 and 100.', 'error')
        return redirect(url_for('index'))

    new_grade = Grade(subject=subject, score=score, student_id=student.id)
    db.session.add(new_grade)
    db.session.commit()
    flash(f'Grade for {subject} added successfully for {student.name}.', 'success')
    return redirect(url_for('index'))

@app.route('/student/<int:student_id>')
def view_student_details(student_id):
    """
    Displays the detailed view for a single student.
    """
    student = Student.query.get_or_404(student_id)
    return render_template('student_details.html', student=student)


@app.route('/delete_student/<int:student_id>', methods=['POST'])
def delete_student(student_id):
    """
    Deletes a student and their associated grades from the database.
    """
    student = Student.query.get_or_404(student_id)
    db.session.delete(student)
    db.session.commit()
    flash(f'Student "{student.name}" has been deleted.', 'success')
    return redirect(url_for('index'))


# --- Bonus Feature Routes ---

@app.route('/subject_topper', methods=['GET'])
def subject_topper():
    """
    Finds and displays the top-performing student in a specific subject.
    """
    subject = request.args.get('subject')
    topper = None
    if subject:
        # Query for grades in the specified subject, ordered by score descending
        top_grade = Grade.query.filter_by(subject=subject).order_by(Grade.score.desc()).first()
        if top_grade:
            topper = top_grade.student
            topper.top_subject = subject
            topper.top_score = top_grade.score

    # Get a unique list of all subjects for the dropdown menu
    subjects = sorted(list(set(grade.subject for grade in Grade.query.all())))
    return render_template('subject_topper.html', topper=topper, subjects=subjects, selected_subject=subject)


@app.route('/class_average', methods=['GET'])
def class_average():
    """
    Calculates and displays the class average for a specific subject.
    """
    subject = request.args.get('subject')
    average = None
    if subject:
        grades_for_subject = Grade.query.filter_by(subject=subject).all()
        if grades_for_subject:
            total_score = sum(grade.score for grade in grades_for_subject)
            average = round(total_score / len(grades_for_subject), 2)

    # Get a unique list of all subjects for the dropdown menu
    subjects = sorted(list(set(grade.subject for grade in Grade.query.all())))
    return render_template('class_average.html', average=average, subjects=subjects, selected_subject=subject)

# --- Main execution ---

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)

