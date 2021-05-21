DROP TABLE IF EXISTS students;
DROP TABLE IF EXISTS quizzes;
DROP TABLE IF EXISTS results;

CREATE TABLE students (
s_id INTEGER PRIMARY KEY,
first_name TEXT,
last_name TEXT
);

CREATE TABLE quizzes (
q_id INTEGER PRIMARY KEY,
q_subject TEXT,
num_questions INTEGER,
q_date DATE
);

CREATE TABLE results (
r_id INTEGER PRIMARY KEY,
s_id INTEGER,
q_id INTEGER,
score INTEGER
);

INSERT INTO students (s_id, first_name, last_name) VALUES (1, 'John', 'Smith');
INSERT INTO quizzes (q_id, q_subject, num_questions, q_date) VALUES (1, 'Python Basics', 5, '2015-05-05');
INSERT INTO results (s_id, q_id_score) VALUES (1,1,85);