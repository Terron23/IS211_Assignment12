import sqlite3
import sys

con = sqlite3.connect('homework.db')

with con:

    cur = con.cursor()
    cur.execute("DROP TABLE IF EXISTS students;")
    cur.execute("DROP TABLE IF EXISTS quizzes;")
    cur.execute("DROP TABLE IF EXISTS results;")

    cur.execute("CREATE TABLE students (id INTEGER PRIMARY KEY, first_name TEXT, last_name TEXT);")
    cur.execute("CREATE TABLE quizzes (id INTEGER PRIMARY KEY, quiz_subject TEXT, num_questions INTEGER, quiz_date DATE);")
    cur.execute("CREATE TABLE results (id INTEGER PRIMARY KEY, student_id INTEGER, quiz_id INTEGER, score INTEGER);")

    cur.execute("INSERT INTO students VALUES ('King', 'Bach');")
    cur.execute("INSERT INTO students VALUES ('Serena', 'Williams');")
    cur.execute("INSERT INTO students VALUES ('Stephy', 'Graft');")
    cur.execute("INSERT INTO students VALUES ('Terron', 'Johnson');")
    cur.execute("INSERT INTO students VALUES ('Jack', 'Black');")
    cur.execute("INSERT INTO students VALUES ('Wu', 'Tang');")

    cur.execute("INSERT INTO quizzes (quiz_subject, num_questions, quiz_date) VALUES ('Intro to Algorithims', 19, '2021-05-05');")
    cur.execute("INSERT INTO results (quiz_id, score) VALUES (1, 1, 85);")
    cur.execute("INSERT INTO results (quiz_id, score) VALUES (1, 2, 85);")
    cur.execute("INSERT INTO results (quiz_id, score) VALUES (1, 3, 85);")
    cur.execute("INSERT INTO results (quiz_id, score) VALUES (1, 4, 85);")
    cur.execute("INSERT INTO results (quiz_id, score) VALUES (1, 5, 85);")
    cur.execute("INSERT INTO results (quiz_id, score) VALUES (1, 6, 85);")