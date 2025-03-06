from config import config
import sqlite3 as sql3
from datetime import datetime

conn = sql3.connect("college_db",check_same_thread=False)
cur = conn.cursor()

def createTables():
    cur.execute("""PRAGMA foreign_keys = ON""")
    cur.execute("""
                CREATE TABLE IF NOT EXISTS department(DEP_ID TEXT NT NULL PRIMARY KEY,
                Name TEXT NOT NULL,
                C_ID TEXT NOT NULL,
                FOREIGN KEY(C_ID) REFERENCES course(C_ID))""")
    cur.execute("""
                CREATE TABLE IF NOT EXISTS course(C_ID TEXT NOT NULL PRIMARY KEY,
                Name TEXT NOT NULL,
                Duration INTEGER)""")
    cur.execute("""
                CREATE TABLE IF NOT EXISTS semester(SEM_ID INTEGER NOT NULL PRIMARY KEY,
                Name TEXT NOT NULL)""")
    cur.execute("""
                CREATE TABLE IF NOT EXISTS subject(SUB_ID TEXT NOT NULL PRIMARY KEY,
                Name TEXT NOT NULL,
                C_ID TEXT NOT NULL,
                SEM INTEGER NOT NULL,
                B_ID TEXT NOT NULL,
                FOREIGN KEY(C_ID) REFERENCES course(C_ID),
                FOREIGN KEY(SEM) REFERENCES semester(SEM_ID),
                FOREIGN KEY(B_ID) REFERENCES department(DEP_ID))""")
    cur.execute("""
                CREATE TABLE IF NOT EXISTS student(ROLL_NO INTEGER NOT NULL PRIMARY KEY,
                Name TEXT NOT NULL,
                DOB TIMESTAMP,
                Gender TEXT)""")
    cur.execute("""
                CREATE TABLE IF NOT EXISTS faculty(FACULTY_ID TEXT NOT NULL PRIMARY KEY,
                Name TEXT NOT NULL,
                Gender TEXT,
                C_ID TEXT NOT NULL,
                FOREIGN KEY(C_ID) REFERENCES course(C_ID))""")
    cur.execute("""
                CREATE TABLE IF NOT EXISTS enrollment(ENROLL_ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                Date TIMESTAMP,
                S_ID INTEGER NOT NULL,
                C_ID TEXT NOT NULL,
                B_ID TEXT NOT NULL,
                FOREIGN KEY(S_ID) REFERENCES student(ROLL_NO),
                FOREIGN KEY(C_ID) REFERENCES course(C_ID),
                FOREIGN KEY(B_ID) REFERENCES department(DEP_ID))""")
    cur.execute("""
                CREATE TABLE IF NOT EXISTS lecture(LEC_ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                F_ID TEXT NOT NULL,
                S_ID TEXT NOT NULL,
                FOREIGN KEY(S_ID) REFERENCES subject(SUB_ID),
                FOREIGN KEY(F_ID) REFERENCES faculty(FACULTY_ID))""")
    conn.commit()


def commit_and_close():
    conn.commit()

# Department CRUD Operations
def create_branch(dep_id, name, c_id):
    cur.execute("INSERT INTO department (DEP_ID, Name, C_ID) VALUES (?, ?, ?)", (dep_id, name, c_id))
    commit_and_close()

def get_all_branches():
    cur.execute("SELECT * FROM department")
    return cur.fetchall()

# Course CRUD Operations
def create_course(c_id, name, duration, dep_id):
    cur.execute("INSERT INTO course (C_ID, Name, Duration) VALUES (?, ?, ?)", (c_id, name, duration))
    commit_and_close()

def get_all_courses():
    cur.execute("SELECT * FROM course")
    return cur.fetchall()

# Semester CRUD Operations
def create_semester(sem_id, name):
    cur.execute("INSERT INTO semester (SEM_ID, Name) VALUES (?, ?)", (sem_id, name))
    commit_and_close()

# Subject CRUD Operations
def create_subject(sub_id, name, c_id, sem, b_id):
    cur.execute("INSERT INTO subject (SUB_ID, Name, C_ID, SEM, B_ID) VALUES (?, ?, ?, ?, ?)", (sub_id, name, c_id, sem, b_id))
    commit_and_close()

def get_all_subjects():
    cur.execute("SELECT * FROM subject")
    return cur.fetchall()

# Student CRUD Operations
def create_student(roll_no, name, dob, gender):
    cur.execute("INSERT INTO student (ROLL_NO, Name, DOB, Gender) VALUES (?, ?, ?, ?)", 
                (roll_no, name, dob, gender))
    commit_and_close()

def get_all_students():
    cur.execute("SELECT * FROM student")
    return cur.fetchall()

# Faculty CRUD Operations
def create_faculty(faculty_id, name, gender, c_id):
    cur.execute("INSERT INTO faculty (FACULTY_ID, Name, Gender, C_ID) VALUES (?, ?, ?, ?)", 
                (faculty_id, name, gender, c_id))
    commit_and_close()

def get_all_faculty():
    cur.execute("SELECT * FROM faculty")
    return cur.fetchall()

def delete_faculty(faculty_id):
    cur.execute("DELETE FROM faculty WHERE FACULTY_ID = ?", (faculty_id,))
    commit_and_close()

# Enrollment CRUD Operations
def create_enrollment(s_id, c_id, b_id):
    cur.execute("INSERT INTO enrollment (S_ID, C_ID, B_ID, Date) VALUES (?, ?, ?)", 
                (s_id, c_id, b_id, datetime.now()))
    commit_and_close()

def get_all_enrollments():
    cur.execute("SELECT * FROM enrollment")
    return cur.fetchall()


# Lecture CRUD Operations
def create_lecture(faculty_id, subject_id):
    cur.execute("INSERT INTO lecture (F_ID, S_ID) VALUES (?, ?)", (faculty_id, subject_id))
    commit_and_close()

def get_all_lectures():
    cur.execute("SELECT * FROM lecture")
    return cur.fetchall()
  
#  Department with Courses (Join department and course)  
def get_departments_with_courses():
    cur.execute("""
        SELECT department.Name AS Department, course.Name AS Course, course.Duration 
        FROM department 
        JOIN course ON department.DEP_ID = course.DEP_ID
    """)
    return cur.fetchall()
def get_all_branches_by_course(c_id):
    cur.execute("SELECT * FROM department WHERE C_ID = ?",(c_id,))
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

def get_total_students():
    cur.execute("SELECT COUNT(*) FROM student")
    return cur.fetchone()[0]
def get_total_female_students():
    cur.execute("SELECT COUNT(*) FROM student where gender='Female'")
    return cur.fetchone()[0]
def get_total_male_students():
    cur.execute("SELECT COUNT(*) FROM student where gender='Male'")
    return cur.fetchone()[0]
def get_total_faculties():
    cur.execute("SELECT COUNT(*) FROM faculty")
    return cur.fetchone()[0]
def get_total_female_faculties():
    cur.execute("SELECT COUNT(*) FROM faculty where gender='Female'")
    return cur.fetchone()[0]
def get_total_male_faculties():
    cur.execute("SELECT COUNT(*) FROM faculty where gender='Male'")
    return cur.fetchone()[0]
def get_total_branches():
    cur.execute("SELECT COUNT(*) FROM department")
    return cur.fetchone()[0]
def get_total_courses():
    cur.execute("SELECT COUNT(*) FROM course")
    return cur.fetchone()[0]