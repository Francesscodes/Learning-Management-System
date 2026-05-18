Learning Management System

A command-line Learning Management System (LMS) built with Python and MySQL, designed to manage students, courses, and enrollments.
Features

- Add and manage students
- Add and manage courses
- Enroll students into courses
- View a student's enrolled courses
- Secure student login with bcrypt password hashing

---
Tech Stack

- Python 3.13
- MySQL — relational database
- mysql-connector-python — database connection
- bcrypt — password hashing

---

 Getting Started

 1. Clone the repository

```bash
git clone https://github.com/Francesscodes/lms-app.git
cd lms-app
```

 2. Create and activate a virtual environment

```bash
python -m venv .venv
.venv\Scripts\activate      # Windows
```

 3. Install dependencies

```bash
pip install mysql-connector-python bcrypt
```

 4. Set up the database

Open MySQL and run the schema file:

```bash
mysql -u root -p < create-db-template.sql
```

 5. Update your database credentials

Open `db.py` and update:

```python
db = mysql_connector.connect(
    host="localhost",
    user="root",
    password="your_password_here",
    database="LMS_DB"
)
```

 6. Run the app

```bash
python main.py
```

---

Database Schema

| Table         | Description                              |
|---------------|------------------------------------------|
| `students`    | Stores student info and hashed passwords |
| `courses`     | Stores course details and instructors    |
| `enrollments` | Junction table linking students to courses |

---

Sample Usage
LMS Menu ---

Add Student
Add Course
Enroll Student in Course
Show Student Courses
Student Login
Exit
