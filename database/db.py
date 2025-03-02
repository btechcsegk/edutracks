from config import config
import sqlite3 as sql3
from datetime import datetime

conn = sql3.connect("college_db",check_same_thread=False)
cur = conn.cursor()

def createTables():
    cur.execute("""PRAGMA foreign_keys = ON""")
    cur.execute("""
                CREATE TABLE IF NOT EXISTS department(DEP_ID TEXT NOT NULL PRIMARY KEY,
                Name TEXT NOT NULL
                )""")
    cur.execute("""
                CREATE TABLE IF NOT EXISTS course(C_ID TEXT NOT NULL PRIMARY KEY,
                Name TEXT NOT NULL,
                Duration INTEGER,
                DEP_ID TEXT NOT NULL,
                FOREIGN KEY(DEP_ID) REFERENCES department(DEP_ID)
                )""")
    cur.execute("""
                CREATE TABLE IF NOT EXISTS semester(SEM_ID INTEGER NOT NULL PRIMARY KEY,
                Name TEXT NOT NULL
                )""")
    cur.execute("""
                CREATE TABLE IF NOT EXISTS subject(SUB_ID TEXT NOT NULL PRIMARY KEY,
                Name TEXT NOT NULL,
                C_ID TEXT NOT NULL,
                SEM INTEGER NOT NULL,
                FOREIGN KEY(C_ID) REFERENCES course(C_ID),
                FOREIGN KEY(SEM) REFERENCES semester(SEM_ID)
                )""")
    cur.execute("""
                CREATE TABLE IF NOT EXISTS student(ROLL_NO INTEGER NOT NULL PRIMARY KEY,
                Name TEXT NOT NULL,
                DOB TIMESTAMP,
                Gender TEXT,
                SEM INTEGER,
                FOREIGN KEY(SEM) REFERENCES semester(SEM_ID)
                )""")
    cur.execute("""
                CREATE TABLE IF NOT EXISTS faculty(FACULTY_ID TEXT NOT NULL PRIMARY KEY,
                Name TEXT NOT NULL,
                Gender TEXT,
                DEP_ID TEXT NOT NULL,
                FOREIGN KEY(DEP_ID) REFERENCES department(DEP_ID)
                )""")
    cur.execute("""
                CREATE TABLE IF NOT EXISTS enrollment(ENROLL_ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                Date TIMESTAMP,
                S_ID INTEGERNOT NULL,
                C_ID TEXT NOT NULL,
                FOREIGN KEY(S_ID) REFERENCES student(ROLL_NO),
                FOREIGN KEY(C_ID) REFERENCES course(C_ID)
                )""")
    cur.execute("""
                CREATE TABLE IF NOT EXISTS lecture(LEC_ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                F_ID TEXT NOT NULL,
                S_ID TEXT NOT NULL,
                FOREIGN KEY(S_ID) REFERENCES subject(SUB_ID),
                FOREIGN KEY(F_ID) REFERENCES faculty(FACULTY_ID)
                )""")
    conn.commit()


def commit_and_close():
    conn.commit()

# Department CRUD Operations
def create_department(dep_id, name):
    cur.execute("INSERT INTO department (DEP_ID, Name) VALUES (?, ?)", (dep_id, name))
    commit_and_close()

def get_all_departments():
    cur.execute("SELECT * FROM department")
    return cur.fetchall()

def update_department(dep_id, new_name):
    cur.execute("UPDATE department SET Name = ? WHERE DEP_ID = ?", (new_name, dep_id))
    commit_and_close()

def delete_department(dep_id):
    cur.execute("DELETE FROM department WHERE DEP_ID = ?", (dep_id,))
    commit_and_close()

# Course CRUD Operations
def create_course(c_id, name, duration, dep_id):
    cur.execute("INSERT INTO course (C_ID, Name, Duration, DEP_ID) VALUES (?, ?, ?, ?)", (c_id, name, duration, dep_id))
    commit_and_close()

def get_all_courses():
    cur.execute("SELECT * FROM course")
    return cur.fetchall()

def update_course(c_id, new_name, new_duration, new_dep_id):
    cur.execute("UPDATE course SET Name = ?, Duration = ?, DEP_ID = ? WHERE C_ID = ?", 
                (new_name, new_duration, new_dep_id, c_id))
    commit_and_close()

def delete_course(c_id):
    cur.execute("DELETE FROM course WHERE C_ID = ?", (c_id,))
    commit_and_close()

# Semester CRUD Operations
def create_semester(sem_id, name):
    cur.execute("INSERT INTO semester (SEM_ID, Name) VALUES (?, ?)", (sem_id, name))
    commit_and_close()

def get_all_semesters():
    cur.execute("SELECT * FROM semester")
    return cur.fetchall()

def update_semester(sem_id, new_name):
    cur.execute("UPDATE semester SET Name = ? WHERE SEM_ID = ?", (new_name, sem_id))
    commit_and_close()

def delete_semester(sem_id):
    cur.execute("DELETE FROM semester WHERE SEM_ID = ?", (sem_id,))
    commit_and_close()

# Subject CRUD Operations
def create_subject(sub_id, name, c_id, sem):
    cur.execute("INSERT INTO subject (SUB_ID, Name, C_ID, SEM) VALUES (?, ?, ?, ?)", (sub_id, name, c_id, sem))
    commit_and_close()

def get_all_subjects():
    cur.execute("SELECT * FROM subject")
    return cur.fetchall()

def update_subject(sub_id, new_name, new_c_id, new_sem):
    cur.execute("UPDATE subject SET Name = ?, C_ID = ?, SEM = ? WHERE SUB_ID = ?", 
                (new_name, new_c_id, new_sem, sub_id))
    commit_and_close()

def delete_subject(sub_id):
    cur.execute("DELETE FROM subject WHERE SUB_ID = ?", (sub_id,))
    commit_and_close()

# Student CRUD Operations
def create_student(roll_no, name, dob, gender, sem):
    cur.execute("INSERT INTO student (ROLL_NO, Name, DOB, Gender, SEM) VALUES (?, ?, ?, ?, ?)", 
                (roll_no, name, dob, gender, sem))
    commit_and_close()

def get_all_students():
    cur.execute("SELECT * FROM student")
    return cur.fetchall()

def update_student(roll_no, new_name, new_dob, new_gender, new_sem):
    cur.execute("UPDATE student SET Name = ?, DOB = ?, Gender = ?, SEM = ? WHERE ROLL_NO = ?", 
                (new_name, new_dob, new_gender, new_sem, roll_no))
    commit_and_close()

def delete_student(roll_no):
    cur.execute("DELETE FROM student WHERE ROLL_NO = ?", (roll_no,))
    commit_and_close()

# Faculty CRUD Operations
def create_faculty(faculty_id, name, gender, c_id):
    cur.execute("INSERT INTO faculty (FACULTY_ID, Name, Gender, C_ID) VALUES (?, ?, ?, ?)", 
                (faculty_id, name, gender, c_id))
    commit_and_close()

def get_all_faculty():
    cur.execute("SELECT * FROM faculty")
    return cur.fetchall()

def update_faculty(faculty_id, new_name, new_gender, new_dep_id):
    cur.execute("UPDATE faculty SET Name = ?, Gender = ?, DEP_ID = ? WHERE FACULTY_ID = ?", 
                (new_name, new_gender, new_dep_id, faculty_id))
    commit_and_close()

def delete_faculty(faculty_id):
    cur.execute("DELETE FROM faculty WHERE FACULTY_ID = ?", (faculty_id,))
    commit_and_close()

# Enrollment CRUD Operations
def create_enrollment(s_id, c_id):
    cur.execute("INSERT INTO enrollment (S_ID, C_ID, Date) VALUES (?, ?, ?)", 
                (s_id, c_id, datetime.now()))
    commit_and_close()

def get_all_enrollments():
    cur.execute("SELECT * FROM enrollment")
    return cur.fetchall()

def delete_enrollment(enroll_id):
    cur.execute("DELETE FROM enrollment WHERE ENROLL_ID = ?", (enroll_id,))
    commit_and_close()

# Lecture CRUD Operations
def create_lecture(faculty_id, subject_id):
    cur.execute("INSERT INTO lecture (F_ID, S_ID) VALUES (?, ?)", (faculty_id, subject_id))
    commit_and_close()

def get_all_lectures():
    cur.execute("SELECT * FROM lecture")
    return cur.fetchall()

def delete_lecture(lec_id):
    cur.execute("DELETE FROM lecture WHERE LEC_ID = ?", (lec_id,))
    commit_and_close()
  
#  Department with Courses (Join department and course)  
def get_departments_with_courses():
    cur.execute("""
        SELECT department.Name AS Department, course.Name AS Course, course.Duration 
        FROM department 
        JOIN course ON department.DEP_ID = course.DEP_ID
    """)
    return cur.fetchall()

# Course with Subjects (Join course and subject)
def get_courses_with_subjects():
    cur.execute("""
        SELECT course.Name AS Course, subject.Name AS Subject, semester.Name AS Semester
        FROM course
        JOIN subject ON course.C_ID = subject.C_ID
        JOIN semester ON subject.SEM = semester.SEM_ID
    """)
    return cur.fetchall()

# Faculty with Department (Join faculty and department)
def get_faculty_with_department():
    cur.execute("""
        SELECT faculty.Name AS Faculty, department.Name AS Department
        FROM faculty
        JOIN department ON faculty.DEP_ID = department.DEP_ID
    """)
    return cur.fetchall()

# Student with Enrollment (Join student and enrollment)
def get_students_with_enrollment():
    cur.execute("""
        SELECT student.Name AS Student, enrollment.Date AS Enrollment_Date, course.Name AS Course
        FROM student
        JOIN enrollment ON student.ROLL_NO = enrollment.S_ID
        JOIN course ON enrollment.C_ID = course.C_ID
    """)
    return cur.fetchall()

# Lecture with Faculty and Subject (Join lecture, faculty, and subject)
def get_lectures_with_faculty_and_subject():
    cur.execute("""
        SELECT lecture.LEC_ID, faculty.Name AS Faculty, subject.Name AS Subject
        FROM lecture
        JOIN faculty ON lecture.F_ID = faculty.FACULTY_ID
        JOIN subject ON lecture.S_ID = subject.SUB_ID
    """)
    return cur.fetchall()


# Enrollment with Student and Course (Join enrollment with student and course)
def get_enrollment_with_student_and_course():
    cur.execute("""
        SELECT enrollment.ENROLL_ID, student.Name AS Student, course.Name AS Course, enrollment.Date AS Enrollment_Date
        FROM enrollment
        JOIN student ON enrollment.S_ID = student.ROLL_NO
        JOIN course ON enrollment.C_ID = course.C_ID
    """)
    return cur.fetchall()

def getTotalStudents():
    cur.execute("SELECT COUNT(*) FROM student")
    return cur.fetchone()[0]
def getTotalFaculties():
    cur.execute("SELECT COUNT(*) FROM faculty")
    return cur.fetchone()[0]
def getTotalFemaleFaculties():
    cur.execute("SELECT COUNT(*) FROM faculty where gender='Female'")
    return cur.fetchone()[0]
def getTotalMaleFaculties():
    cur.execute("SELECT COUNT(*) FROM faculty where gender='Male'")
    return cur.fetchone()[0]
def getTotalDepartments():
    cur.execute("SELECT COUNT(*) FROM department")
    return cur.fetchone()[0]
def getTotalCourses():
    cur.execute("SELECT COUNT(*) FROM course")
    return cur.fetchone()[0]