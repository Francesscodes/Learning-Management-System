Learning Management System

A command-line Learning Management System (LMS) built with Python and MySQL, designed to manage students, courses, and enrollments.
Features

- Add and manage students
- Add and manage courses
- Enroll students into courses
- View a student's enrolled courses
- Secure student login with bcrypt password hashing
-  REST API with auto-generated Swagger documentation


---
Tech Stack

-Python 3.13
- MySQL — relational database
- FastAPI — REST API framework
- Uvicorn — ASGI server
- mysql-connector-python — database connection
- bcrypt — password hashing
- Pydantic — request validation

---

Project Structure
Learning-Management-System/

main.py                  # CLI app logic, classes, and menu

api.py                   # FastAPI REST API

db.py                    # MySQL database connection (not committed)

create-db-template.sql   # Database schema and seed data

README.md

 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/Francesscodes/Learning-Management-System.git
cd Learning-Management-System
```

### 2. Create and activate a virtual environment

```bash
python -m venv .venv
.venv\Scripts\activate      # Windows
```

### 3. Install dependencies

```bash
pip install mysql-connector-python bcrypt fastapi uvicorn
```

### 4. Set up the database

```bash
mysql -u root -p < create-db-template.sql
```

### 5. Configure your database connection

Copy `db.example.py` to `db.py` and fill in your credentials:

```python
db = mysql_connector.connect(
    host="localhost",
    user="root",
    password="your_password_here",
    database="LMS_DB"
)
```

### 6. Run the CLI app

```bash
python main.py
```

### 7. Run the REST API

```bash
uvicorn api:app --reload
```

Then open your browser at:
http://127.0.0.1:8000/docs


API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/students` | Get all students |
| `POST` | `/students` | Add a new student |
| `POST` | `/students/login` | Student login |
| `GET` | `/courses` | Get all courses |
| `POST` | `/courses` | Add a new course |
| `POST` | `/enrollments` | Enroll a student in a course |
| `GET` | `/students/{student_name}/courses` | Get a student's enrolled courses |

Full interactive documentation available at `/docs` when the API is running.


---

Database Schema

| Table         | Description                              |
|---------------|------------------------------------------|
| `students`    | Stores student info and hashed passwords |
| `courses`     | Stores course details and instructors    |
| `enrollments` | Junction table linking students to courses |

---

LMS Menu ---

Add Student
Add Course
Enroll Student in Course
Show Student Courses
Student Login
Exit
