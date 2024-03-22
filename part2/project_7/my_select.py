from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from models import Student, Grade, Subject, Teacher, Group

engine = create_engine('sqlite:///university')

Session = sessionmaker(bind=engine)

session = Session()


def select_1():
    top_5_students = (
        session.query(Student.name, func.avg(Grade.score).label('average_score'))
        .join(Grade)
        .group_by(Student)
        .order_by(func.avg(Grade.score).desc())
        .limit(5)
        .all()
    )
    return top_5_students



def select_2(subject_name):
    top_student = (
        session.query(Student.name, func.avg(Grade.score).label('average_score'))
        .join(Grade)
        .join(Subject)
        .filter(Subject.name == subject_name)
        .group_by(Student)
        .order_by(func.avg(Grade.score).desc())
        .first()
    )
    return top_student



def select_3(subject_name):
    avg_scores_by_group = (
        session.query(Group.name, func.avg(Grade.score).label('average_score'))
        .select_from(Group)
        .join(Student)
        .join(Grade)
        .join(Subject)
        .filter(Subject.name == subject_name)
        .group_by(Group)
        .all()
    )
    return avg_scores_by_group



def select_4():
    avg_score_overall = (
        session.query(func.avg(Grade.score).label('average_score'))
        .select_from(Grade)
        .scalar()
    )
    return avg_score_overall


def select_5(teacher_name):
    courses_taught_by_teacher = (
        session.query(Subject.name)
        .select_from(Subject)
        .join(Teacher)
        .filter(Teacher.name == teacher_name)
        .all()
    )
    return courses_taught_by_teacher


def select_6(group_name):
    students_in_group = (
        session.query(Student.name)
        .select_from(Student)
        .join(Group)
        .filter(Group.name == group_name)
        .all()
    )
    return students_in_group


def select_7(group_name, subject_name):
    grades_in_group_by_subject = (
        session.query(Student.name, Grade.score)
        .select_from(Student)
        .join(Group)
        .join(Grade)
        .join(Subject)
        .filter(Group.name == group_name, Subject.name == subject_name)
        .all()
    )
    return grades_in_group_by_subject


def select_8(teacher_name):
    avg_score_by_teacher = (
        session.query(func.avg(Grade.score).label('average_score'))
        .select_from(Grade)
        .join(Subject)
        .join(Teacher)
        .filter(Teacher.name == teacher_name)
        .scalar()
    )
    return avg_score_by_teacher


def select_9(student_name):
    courses_attended_by_student = (
        session.query(Subject.name)
        .select_from(Subject)
        .join(Grade)
        .join(Student)
        .filter(Student.name == student_name)
        .all()
    )
    return courses_attended_by_student


def select_10(student_name, teacher_name):
    courses_taught_to_student_by_teacher = (
        session.query(Subject.name)
        .select_from(Subject)
        .join(Grade)
        .join(Student)
        .join(Teacher)
        .filter(Student.name == student_name, Teacher.name == teacher_name)
        .all()
    )
    return courses_taught_to_student_by_teacher


print(select_1())
print(select_2('reality'))
print(select_3('talk'))
print(select_4())
print(select_5('Erik Johnson'))
print(select_6('Group 1'))
print(select_7('Group 1', 'week'))
print(select_8('Erik Johnson'))
print(select_9('Linda Marshall'))
print(select_10('Robert Adams', 'Erik Johnson'))


