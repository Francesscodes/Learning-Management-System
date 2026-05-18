from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from db import db, cursor
import bcrypt
from datetime import date

app = FastAPI(title="LMS API", version="1.0.0")


# ─────────────────────────────────────────
# SCHEMAS (request bodies)
# ─────────────────────────────────────────

class StudentCreate(BaseModel):
    name: str
    email: str
    password: str
    enrollment_date: date
    courses: str = ""

class StudentLogin(BaseModel):
    email: str
    password: str

class CourseCreate(BaseModel):
    name: str
    description: str
    instructor: str
    start_date: date
    end_date: date

class EnrollmentCreate(BaseModel):
    student_name: str
    course_name: str


# ─────────────────────────────────────────
# STUDENTS
# ─────────────────────────────────────────

@app.post("/students", status_code=201)
def add_student(student: StudentCreate):
    try:
        hashed = bcrypt.hashpw(student.password.encode("utf-8"), bcrypt.gensalt())
        cursor.execute(
            """INSERT INTO students
               (student_name, student_email, student_password,
                student_enrollment_date, student_courses)
               VALUES (%s, %s, %s, %s, %s)""",
            (student.name, student.email, hashed,
             student.enrollment_date, student.courses)
        )
        db.commit()
        return {"message": f"Student '{student.name}' added successfully."}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/students")
def get_all_students():
    cursor.execute(
        "SELECT student_id, student_name, student_email, student_enrollment_date FROM students"
    )
    rows = cursor.fetchall()
    return [
        {
            "id": r[0],
            "name": r[1],
            "email": r[2],
            "enrollment_date": r[3]
        }
        for r in rows
    ]


@app.post("/students/login")
def login_student(credentials: StudentLogin):
    cursor.execute(
        "SELECT student_name, student_password FROM students WHERE student_email = %s",
        (credentials.email,)
    )
    row = cursor.fetchone()

    if not row:
        raise HTTPException(status_code=404, detail="No account found with that email.")

    stored_hash = row[1]
    if isinstance(stored_hash, str):
        stored_hash = stored_hash.encode("utf-8")

    if bcrypt.checkpw(credentials.password.encode("utf-8"), stored_hash):
        return {"message": f"Welcome back, {row[0]}!"}
    else:
        raise HTTPException(status_code=401, detail="Incorrect password.")


# ─────────────────────────────────────────
# COURSES
# ─────────────────────────────────────────

@app.post("/courses", status_code=201)
def add_course(course: CourseCreate):
    try:
        cursor.execute(
            """INSERT INTO courses
               (course_name, course_description, course_instructor,
                course_start_date, course_end_date)
               VALUES (%s, %s, %s, %s, %s)""",
            (course.name, course.description, course.instructor,
             course.start_date, course.end_date)
        )
        db.commit()
        return {"message": f"Course '{course.name}' added successfully."}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/courses")
def get_all_courses():
    cursor.execute(
        "SELECT course_id, course_name, course_description, course_instructor, course_start_date, course_end_date FROM courses"
    )
    rows = cursor.fetchall()
    return [
        {
            "id": r[0],
            "name": r[1],
            "description": r[2],
            "instructor": r[3],
            "start_date": r[4],
            "end_date": r[5]
        }
        for r in rows
    ]


# ─────────────────────────────────────────
# ENROLLMENTS
# ─────────────────────────────────────────

@app.post("/enrollments", status_code=201)
def enroll_student(enrollment: EnrollmentCreate):
    cursor.execute(
        "SELECT student_id FROM students WHERE student_name = %s",
        (enrollment.student_name,)
    )
    student = cursor.fetchone()

    cursor.execute(
        "SELECT course_id FROM courses WHERE course_name = %s",
        (enrollment.course_name,)
    )
    course = cursor.fetchone()

    if not student:
        raise HTTPException(status_code=404, detail="Student not found.")
    if not course:
        raise HTTPException(status_code=404, detail="Course not found.")

    try:
        cursor.execute(
            "INSERT INTO enrollments (student_id, course_id) VALUES (%s, %s)",
            (student[0], course[0])
        )
        db.commit()
        return {"message": f"'{enrollment.student_name}' enrolled in '{enrollment.course_name}' successfully."}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/students/{student_name}/courses")
def get_student_courses(student_name: str):
    cursor.execute(
        """SELECT c.course_id, c.course_name, c.course_description,
                  c.course_instructor, c.course_start_date, c.course_end_date
           FROM enrollments e
           JOIN students s ON e.student_id = s.student_id
           JOIN courses  c ON e.course_id  = c.course_id
           WHERE s.student_name = %s""",
        (student_name,)
    )
    rows = cursor.fetchall()

    if not rows:
        raise HTTPException(status_code=404, detail=f"No courses found for '{student_name}'.")

    return [
        {
            "id": r[0],
            "name": r[1],
            "description": r[2],
            "instructor": r[3],
            "start_date": r[4],
            "end_date": r[5]
        }
        for r in rows
    ]