from faker import Faker
import random
import sqlite3
from datetime import datetime, timedelta
fake = Faker()

con = sqlite3.connect('./main.db')
cur = con.cursor()

groups = []
#create groups
for i in range(1,4):
    groups.append(
        {
            'name' : f'group {i}'
        }
    )
#create lectors
lectors = []
for i in range(6):
    lectors.append(
        {
            'name' : fake.name(),
            'lastname' : fake.last_name()
        }
    )

#create subjects
subjects = []
for i in range(8):
    subjects.append(
        {
            'name' : fake.job(),
            'lector_id': random.randint(1, 6)
        }
    )
#create students
students = []
for i in range(30):
    students.append(
        {
            'lastname' : fake.last_name(),
            'name' : fake.name(),
            'group_id': random.choice(groups)['name']
        }
    )
#create marks
marks = []
for student_id in range(1, 31):
    for i in range(20):
        marks.append(
            {
                'student_id' : student_id,
                'subject_id' : random.randint(1, 8),
                'mark' : random.randint(1,12),
                'date' : (datetime.today() - timedelta(days=random.randint(1, 150))).strftime("%Y-%m-%d")
            }
        )

# print(marks)
# Insert data into tables
cur.executemany("INSERT INTO groups (name) VALUES (:name)", groups)
cur.executemany("INSERT INTO lectors (name, lastname) VALUES (:name, :lastname)", lectors)
cur.executemany("INSERT INTO subjects (name, lector_id) VALUES (:name, :lector_id)", subjects)
cur.executemany("INSERT INTO students (lastname, name, group_id) VALUES (:lastname, :name, :group_id)", students)
cur.executemany("""
INSERT INTO marks (student_id, subject_id, mark, date)
VALUES (:student_id, :subject_id, :mark, :date)""", marks)
con.commit()

print("Database populated successfully!")