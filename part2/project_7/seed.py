from faker import Faker
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Student, Group, Teacher, Subject, Grade
from sqlalchemy.exc import IntegrityError
import random
from datetime import datetime, timedelta


engine = create_engine('sqlite:///university')
Session = sessionmaker(bind=engine)
session = Session()

fake = Faker()


def generate_data():
    groups = [Group(name=f"Group {i}") for i in range(1, 4)]
    session.add_all(groups)
    session.commit()

    teachers = [Teacher(name=fake.name()) for _ in range(3)]
    session.add_all(teachers)
    session.commit()

    subjects = []
    for _ in range(5):
        teacher = random.choice(teachers)
        subject = Subject(name=fake.word(), teacher_id=teacher.id)
        subjects.append(subject)
        session.add(subject)
    session.commit()

    students = []
    for _ in range(30):
        student = Student(name=fake.name(), group_id=random.choice(groups).id)
        students.append(student)
        session.add(student)
    session.commit()


    for student in students:
        for subject in subjects:
            score = random.randint(60, 100)
            date = datetime.now() - timedelta(days=random.randint(0, 365))
            grade = Grade(student_id=student.id, subject_id=subject.id, score=score, date=date)
            session.add(grade)
    session.commit()


generate_data()

print("Data seeding completed.")
