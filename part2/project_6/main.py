import sqlite3


con = sqlite3.connect('./main.db')
cur = con.cursor()

def create_tables():
    cur.execute(
        "CREATE TABLE IF NOT EXISTS students (id INTEGER PRIMARY KEY AUTOINCREMENT,"
        "lastname VARCHAR(255) NOT NULL,"
        "name VARCHAR(255) NOT NULL,"
        "group_id INTEGER,"
        "FOREIGN KEY (group_id) REFERENCES groups(id))"
    )
    cur.execute(
        "CREATE TABLE IF NOT EXISTS groups (id INTEGER PRIMARY KEY AUTOINCREMENT,"
        "name VARCHAR(255) NOT NULL)"
    )
    cur.execute(
        "CREATE TABLE IF NOT EXISTS lectors (id INTEGER PRIMARY KEY AUTOINCREMENT,"
        "name VARCHAR(255) NOT NULL,"
        "lastname VARCHAR(255) NOT NULL)"
    )
    cur.execute(
        "CREATE TABLE IF NOT EXISTS subjects (id INTEGER PRIMARY KEY AUTOINCREMENT,"
        "name VARCHAR(255) NOT NULL,"
        "lector_id INTEGER,"
        "FOREIGN KEY (lector_id) REFERENCES lectors(id))"
    )
    cur.execute(
        "CREATE TABLE IF NOT EXISTS marks (id INTEGER PRIMARY KEY AUTOINCREMENT,"
        "student_id INTEGER,"
        "subject_id INTEGER,"
        "mark INTEGER,"
        "date DATE,"
        "FOREIGN KEY (student_id) REFERENCES students(id),"
        "FOREIGN KEY (subject_id) REFERENCES subjects(id))"
    )
    con.commit()


if __name__ == '__main__':
    queries = [
        "query_1.sql",
        "query_2.sql",
        "query_3.sql",
        "query_4.sql",
        "query_5.sql",
        "query_6.sql",
        "query_7.sql",
        "query_8.sql",
        "query_9.sql",
        "query_10.sql"
    ]

    for query_file in queries:
        with open(query_file, 'r') as file:
            query = file.read()
            cur.execute(query)
            rows = cur.fetchall()
            print(f"Results for {query_file}:")
            print(rows)


    con.close()
