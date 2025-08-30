Student Performance Tracker
This web application allows teachers to track student performance across different subjects. It provides a user-friendly interface to add students, assign grades, view details, and calculate average scores.

How to Use the Web Application
1. Main Dashboard
When you open the application, you will see the main dashboard. It has two main sections:

Add a New Student: A form on the left to add new students to the system.

Student Roster: A list on the right displaying all existing students.

2. Adding a Student
To add a new student:

Navigate to the "Add a New Student" form.

Enter the student's Full Name.

Enter a unique Roll Number.

Click the "Add Student" button.
The new student will appear in the "Student Roster".

3. Assigning Grades
To assign a grade to a student:

Find the student in the "Student Roster".

In the "Add Grade" section for that student, enter the Subject (e.g., Math, Science).

Enter the Score (must be a number between 0 and 100).

Click the "Add Grade" button.
The grade will be added to the student's record and their average score will update automatically.

4. Viewing Student Details
The main roster shows a summary for each student, including their current grades and average score.

5. Deleting a Student
To remove a student from the system:

Find the student in the "Student Roster".

Click the "Delete" button next to their name.

A confirmation prompt will appear. Confirm the action to permanently delete the student and all their associated grades.

6. Advanced Reports (Bonus Features)
The application includes two advanced reporting tools accessible from the main page:

Find Subject Topper:

Click the "Find Subject Topper" button.

Select a subject from the dropdown list.

Click "Find Topper".

The application will display the student with the highest score in that subject.

Calculate Class Average:

Click the "Calculate Class Average" button.

Select a subject from the dropdown list.

Click "Calculate".

The application will display the average score of all students in that specific subject.

Local Setup and Deployment
Running Locally
Install Dependencies: pip install -r requirements.txt

Run the App: python app.py

Open your browser and go to http://127.0.0.1:5000

Deployment
This application is ready for deployment on platforms like Heroku. The repository includes:

requirements.txt: Lists all necessary Python packages.

Procfile: Specifies the command (gunicorn app:app) to start the web server for a production environment.

To deploy, you would typically push this code to a Git repository and link it to your hosting service.