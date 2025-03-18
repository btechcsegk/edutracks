from config import config
import sqlite3 as sql3
from datetime import datetime

conn = sql3.connect("college_db",check_same_thread=False)
cur = conn.cursor()
# cur.execute("""PRAGMA foreign_keys = ON""")
def createTables():
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
                SEM INTEGER NOT NULL,
                FOREIGN KEY(S_ID) REFERENCES student(ROLL_NO),
                FOREIGN KEY(C_ID) REFERENCES course(C_ID),
                FOREIGN KEY(B_ID) REFERENCES department(DEP_ID),
                FOREIGN KEY(SEM) REFERENCES semester(SEM_ID))""")
    cur.execute("""
                CREATE TABLE IF NOT EXISTS lecture(LEC_ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                F_ID TEXT NOT NULL,
                S_ID TEXT NOT NULL,
                FOREIGN KEY(S_ID) REFERENCES subject(SUB_ID),
                FOREIGN KEY(F_ID) REFERENCES faculty(FACULTY_ID))""")
    cur.execute("""
                CREATE TABLE IF NOT EXISTS attendance(A_ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                OBT INTEGER DEFAULT 0,
                SUB_ID TEXT NOT NULL,
                S_ID TEXT NOT NULL,
                FOREIGN KEY(SUB_ID) REFERENCES subject(SUB_ID),
                FOREIGN KEY(S_ID) REFERENCES student(ROLL_NO))""")
    cur.execute("""
                CREATE TABLE IF NOT EXISTS exam(E_ID TEXT NOT NULL PRIMARY KEY,
                Name TEXT NOT NULL,
                TOT INTEGER NOT NULL,
                SUB_ID TEXT NOT NULL,
                FOREIGN KEY(SUB_ID) REFERENCES subject(SUB_ID))""")
    
    cur.execute("""
                CREATE TABLE IF NOT EXISTS exam_list(EX_ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                OBT INTEGER NOT NULL,
                S_ID INTEGER NOT NULL,
                E_ID TEXT NOT NULL,
                FOREIGN KEY(S_ID) REFERENCES student(ROLL_NO)
                FOREIGN KEY(E_ID) REFERENCES exam(E_ID))""")
    
    cur.execute("""
                CREATE TABLE IF NOT EXISTS sub_attendance(SA_ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                TOT INTEGER NOT NULL,
                SUB_ID TEXT NOT NULL,
                FOREIGN KEY(SUB_ID) REFERENCES subject(SUB_ID))""")
    
    conn.commit()

def commit_and_close():
    conn.commit()


def get_exams_data():
    cur.execute("Select e_id, count(*) from exam_list group by e_id")
    return cur.fetchall()

def get_att_by_s_id_and_sem(s_id):
    cur.execute(f"Select subject.name,attendance.obt,sub_attendance.tot from sub_attendance INNER JOIN attendance ON sub_attendance.sub_id=attendance.sub_id INNER JOIN subject ON attendance.sub_id=subject.sub_id INNER JOIN enrollment ON subject.sem=subject.sem where enrollment.s_id={s_id}")
    return cur.fetchall()

def get_marks_subject_wise(uid):
    cur.execute(f"SELECT exam.name, exam_list.obt,exam.tot from exam INNER JOIN exam_list ON exam.e_id=exam_list.e_id WHERE exam_list.s_id={uid}")
    return cur.fetchall()
def best_in_marks_male_by_sem():
    cur.execute("Select student.name, max(exam_list.obt) from exam_list INNER JOIN student ON exam_list.s_id=student.roll_no where student.gender='Male'")
    return cur.fetchall()

def best_in_marks_female_by_sem():
    cur.execute("Select student.name, max(exam_list.obt) from exam_list INNER JOIN student ON exam_list.s_id=student.roll_no where student.gender='Female'")
    return cur.fetchall()

def best_in_att_male_by_sem(sem):
    cur.execute(f"SELECT student.name, max(attendance.obt) FROM student INNER JOIN enrollment ON student.roll_no = enrollment.s_id INNER JOIN subject ON enrollment.b_id = subject.b_id INNER JOIN attendance ON student.roll_no = attendance.s_id AND subject.sub_id = attendance.sub_id where student.gender='Male' AND subject.sem={sem}")
    return cur.fetchall()

def best_in_att_female_by_sem(sem):
    cur.execute(f"SELECT student.name, max(attendance.obt) FROM student INNER JOIN enrollment ON student.roll_no = enrollment.s_id INNER JOIN subject ON enrollment.b_id = subject.b_id INNER JOIN attendance ON student.roll_no = attendance.s_id AND subject.sub_id = attendance.sub_id where student.gender='Female' AND subject.sem={sem}")
    return cur.fetchall()

def get_details_by_id(stu_id):
    cur.execute(f"Select * from student where roll_no={stu_id}")
    return cur.fetchone()
    
def get_exam_details_by_id(e_id):
    cur.execute(f"Selct * from exam where e_id={e_id}")
    return cur.fetchone()
    
def add_exam(e_id, name, tot, sub_id):
    cur.execute(f"INSERT INTO exam(e_id, name, tot, sub_id) values('{e_id}','{name}', {tot}, '{sub_id}')")
    commit_and_close()
    
def get_average_attendance_by_id(s_id):
    cur.execute(f"Select sum(attendance.OBT), sum(sub_attendance.TOT) FROM attendance INNER JOIN sub_attendance ON attendance.SUB_ID=sub_attendance.SUB_ID where attendance.S_ID={s_id}")
    return cur.fetchone()

def get_semester_by_id(s_id):
    cur.execute(f"Select sem from enrollment where s_id={s_id}")
    return cur.fetchone()

def get_lecture_with_fac():
    cur.execute("SELECT faculty.name, faculty.faculty_id, lecture.s_id from faculty RIGHT JOIN lecture ON faculty.faculty_id=lecture.f_id")
    return cur.fetchall()
def add_mark(s_id, e_id, obt):
    cur.execute(f"INSERT INTO exam_list(obt, s_id, e_id) values({obt},{s_id},'{e_id}')")
    commit_and_close()
    
def update_mark(s_id, e_id, obt):
    cur.execute(f"UPDATE exam_list SET obt={obt} WHERE s_id={s_id} AND e_id='{e_id}'")
    commit_and_close()
    
def checkin_mark_list_by_id(s_id,e_id):
    cur.execute(f"Select count(*) from exam_list where s_id={s_id} and e_id='{e_id}'")
    return cur.fetchone()
def get_mark_by_id(s_id,e_id):
    cur.execute(f"Select obt from exam_list where s_id={s_id} and e_id='{e_id}'")
    return cur.fetchone()
    
def update_attendance_by_id(new_att, s_id, sub_id):
    cur.execute(f"UPDATE attendance SET obt={new_att} WHERE s_id={s_id} AND sub_id='{sub_id}'")
    commit_and_close()
    
def insert_attendance_by_id(new_att, s_id, sub_id):
    cur.execute(f"INSERT INTO attendance(obt, s_id, sub_id) VALUES({new_att},{s_id},'{sub_id}')")
    commit_and_close()
    
def checkin_attendance_list_by_id(s_id,sub_id):
    cur.execute(f"Select count(*) from attendance where s_id={s_id} and sub_id='{sub_id}'")
    return cur.fetchone()

def add_total_attendance(sub_id, tot):
    cur.execute(f"INSERT INTO sub_attendance(tot, sub_id) VALUES({tot},'{sub_id}')")
    commit_and_close()
    
def update_total_attendance(sub_id, tot):
    cur.execute(f"UPDATE sub_attendance set tot={tot} where sub_id='{sub_id}'")
    commit_and_close()

def get_student_list_by_branch(b_id,sem):
    cur.execute("select * from student INNER JOIN enrollment ON student.roll_no = enrollment.s_id where enrollment.b_id = ? AND sem=?",(b_id,sem))
    return cur.fetchall()


def get_subject_count(s_id):
    cur.execute("select count(*) from subject where sem = (select sem from enrollment where s_id=?)",(s_id,))
    return cur.fetchone()

def get_total_att_by_sub_id(sub_id):
    cur.execute("SELECT tot FROM sub_attendance where sub_id=?",(sub_id,))
    return cur.fetchone()

def get_obtained_att_by_sub_and_stu_id(sub_id,s_id):
    cur.execute("SELECT obt FROM attendance WHERE sub_id=? AND s_id=?",(sub_id,s_id))
    return cur.fetchone()

def get_all_sub_by_fac_id(f_id):
    cur.execute("SELECT S_Id from lecture where F_ID = ?",(f_id,))
    return cur.fetchall()
# Department CRUD Operations
def create_branch(dep_id, name, c_id):
    cur.execute("INSERT INTO department (DEP_ID, Name, C_ID) VALUES (?, ?, ?)", (dep_id, name, c_id))
    commit_and_close()

def get_all_branches():
    cur.execute("SELECT * FROM department")
    return cur.fetchall()

def get_exams_by_sub_id(subid):
    cur.execute("SELECT * FROM exam WHERE sub_id=?",(subid,))
    return cur.fetchall()
    
# Course CRUD Operations
def create_course(c_id, name, duration):
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

def get_all_semester():
    cur.execute("SELECT * FROM semester")
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
def create_enrollment(s_id, c_id, b_id, sem):
    cur.execute("INSERT INTO enrollment (S_ID, C_ID, B_ID, SEM, Date) VALUES (?, ?, ?, ?, ?)", 
                (s_id, c_id, b_id, sem, datetime.now()))
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
  

def get_all_branches_by_course(c_id):
    cur.execute("SELECT * FROM department WHERE C_ID = ?",(c_id,))
    return cur.fetchall()






def get_total_marks_by_exam_id(e_id):
    cur.execute("select tot from exam where e_id = ?",(e_id,))
    return cur.fetchone()
def get_total_students():
    cur.execute("SELECT COUNT(*) FROM student")
    return cur.fetchone()[0]
def get_total_students_by_semester(course,sem):
    cur.execute("SELECT COUNT(*) FROM enrollment where C_ID=? AND SEM=?",(course,sem))
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