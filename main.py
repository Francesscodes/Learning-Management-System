from db import db, cursor
from getpass import getpass
import bcrypt


# ─────────────────────────────────────────
# COURSE
# ─────────────────────────────────────────

class Course:

    def __init__(self, course_id, name, description, instructor, start_date, end_date):
        self.course_id   = course_id
        self.name        = name
        self.description = description
        self.instructor  = instructor
        self.start_date  = start_date
        self.end_date    = end_date

    def __str__(self):
        return (f"[{self.course_id}] {self.name} | Instructor: {self.instructor} "
                f"| {self.start_date} → {self.end_date}")


# ─────────────────────────────────────────
# STUDENT
# ─────────────────────────────────────────

class Student:

    def __init__(self, student_id, name, email, enrollment_date, courses=None):
        self.student_id      = student_id
        self.name            = name
        self.email           = email
        self.enrollment_date = enrollment_date
        self.courses         = courses or []

    def show_courses(self):
        if not self.courses:
            print(f"{self.name} is not enrolled in any courses.")
        else:
            print(f"\n{self.name}'s Enrolled Courses:")
            for course in self.courses:
                print(f"  - {course}")


# ─────────────────────────────────────────
# LMS
# ─────────────────────────────────────────

class LMS:

    # ── Students ──────────────────────────

    def add_student(self, name, email, password, enrollment_date, courses=""):
        try:
            hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
            cursor.execute(
                """INSERT INTO students
                   (student_name, student_email, student_password,
                    student_enrollment_date, student_courses)
                   VALUES (%s, %s, %s, %s, %s)""",
                (name, email, hashed, enrollment_date, courses)
            )
            db.commit()
            print(f"Student '{name}' added successfully.")
        except Exception as e:
            print(f"Error adding student: {e}")

    def get_student(self, student_name):
        cursor.execute(
            "SELECT * FROM students WHERE student_name = %s", (student_name,)
        )
        row = cursor.fetchone()
        if row:
            # row order: id, name, email, password, enrollment_date, courses
            return Student(row[0], row[1], row[2], row[4])
        return None

    def login_student(self, email, password):
        cursor.execute(
            "SELECT student_name, student_password FROM students WHERE student_email = %s",
            (email,)
        )
        row = cursor.fetchone()

        if not row:
            print("No account found with that email.")
            return

        stored_hash = row[1]

        # stored_hash may come back as a string depending on your MySQL driver version
        if isinstance(stored_hash, str):
            stored_hash = stored_hash.encode("utf-8")

        if bcrypt.checkpw(password.encode("utf-8"), stored_hash):
            print(f"Welcome back, {row[0]}!")
        else:
            print("Incorrect password.")

    # ── Courses ───────────────────────────

    def add_course(self, name, description, instructor, start_date, end_date):
        try:
            cursor.execute(
                """INSERT INTO courses
                   (course_name, course_description, course_instructor,
                    course_start_date, course_end_date)
                   VALUES (%s, %s, %s, %s, %s)""",
                (name, description, instructor, start_date, end_date)
            )
            db.commit()
            print(f"Course '{name}' added successfully.")
        except Exception as e:
            print(f"Error adding course: {e}")

    def get_course(self, course_name):
        cursor.execute(
            "SELECT * FROM courses WHERE course_name = %s", (course_name,)
        )
        row = cursor.fetchone()
        if row:
            # row order: id, name, description, instructor, start_date, end_date
            return Course(row[0], row[1], row[2], row[3], row[4], row[5])
        return None

    # ── Enrollments ───────────────────────

    def enroll(self, student_name, course_name):
        student = self.get_student(student_name)
        course  = self.get_course(course_name)

        if not student:
            print(f"Student '{student_name}' not found.")
            return
        if not course:
            print(f"Course '{course_name}' not found.")
            return

        try:
            cursor.execute(
                """INSERT INTO enrollments (student_id, course_id)
                   VALUES (%s, %s)""",
                (student.student_id, course.course_id)
            )
            db.commit()
            print(f"'{student_name}' enrolled in '{course_name}' successfully.")
        except Exception as e:
            print(f"Error enrolling student: {e}")

    def show_student_courses(self, student_name):
        cursor.execute(
            """SELECT c.course_id, c.course_name, c.course_description,
                      c.course_instructor, c.course_start_date, c.course_end_date
               FROM enrollments e
               JOIN students  s ON e.student_id = s.student_id
               JOIN courses   c ON e.course_id  = c.course_id
               WHERE s.student_name = %s""",
            (student_name,)
        )
        rows = cursor.fetchall()

        if not rows:
            print(f"No courses found for '{student_name}'.")
            return

        student = self.get_student(student_name)
        if student:
            student.courses = [
                Course(r[0], r[1], r[2], r[3], r[4], r[5]) for r in rows
            ]
            student.show_courses()


# ─────────────────────────────────────────
# MAIN MENU
# ─────────────────────────────────────────

def main():
    lms = LMS()

    while True:
        print("\n--- LMS Menu ---")
        print("1. Add Student")
        print("2. Add Course")
        print("3. Enroll Student in Course")
        print("4. Show Student Courses")
        print("5. Student Login")
        print("6. Exit")

        choice = input("Choose (1-6): ").strip()

        if choice == '1':
            name            = input("Student name: ").strip()
            email           = input("Student email: ").strip()
            password        = getpass("Password: ")
            enrollment_date = input("Enrollment date (YYYY-MM-DD): ").strip()
            courses         = input("Initial course(s) [optional]: ").strip()
            lms.add_student(name, email, password, enrollment_date, courses)

        elif choice == '2':
            name        = input("Course name: ").strip()
            description = input("Course description: ").strip()
            instructor  = input("Instructor name: ").strip()
            start_date  = input("Start date (YYYY-MM-DD): ").strip()
            end_date    = input("End date (YYYY-MM-DD): ").strip()
            lms.add_course(name, description, instructor, start_date, end_date)

        elif choice == '3':
            student_name = input("Student name: ").strip()
            course_name  = input("Course name: ").strip()
            lms.enroll(student_name, course_name)

        elif choice == '4':
            student_name = input("Student name: ").strip()
            lms.show_student_courses(student_name)

        elif choice == '5':
            email    = input("Email: ").strip()
            password = getpass("Password: ")
            lms.login_student(email, password)

        elif choice == '6':
            print("Exiting LMS. Goodbye!")
            break

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()