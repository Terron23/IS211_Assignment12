import sqlite3
from flask import Flask, request, session, g, redirect, render_template


#############
# Using g to handle request
# #################

app = Flask(__name__, template_folder='templates')

app.config['SECRET_KEY'] = 'the random string' 

def connect_db():
    con = sqlite3.connect('homework.db', check_same_thread=False)

    cur = con.cursor()
    cur.execute("CREATE TABLE if not exists students (id INTEGER PRIMARY KEY, first_name TEXT, last_name TEXT);")
    cur.execute("CREATE TABLE if not exists  quizzes (id INTEGER PRIMARY KEY, quiz_subject TEXT, num_questions INTEGER, quiz_date DATE, student_id integer, grade integer);")
    cur.execute("CREATE TABLE if not exists  results (id INTEGER PRIMARY KEY, student_id INTEGER, quiz_id INTEGER, score INTEGER);")
    return con

@app.teardown_appcontext
def close_db(Exception):
    if hasattr(g, 'sqlite_db'):
        g.sqlite3_db.close()

@app.before_request
def before_request():
    g.db = connect_db()

@app.route('/')
def index():
    return redirect('/login')

@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':
        session['username'] = request.form['username']
        username = request.form['username']
        password = request.form['password']

        if username == 'admin' and password == 'password':
            return redirect('/dashboard')
        else:
            return render_template('login.html')
    else:
        return render_template('login.html')

@app.route('/dashboard', methods=['GET'])
def dashboard():
    if session['username']=='admin':

        student_quuery = g.db.execute("SELECT * FROM students")
        quiz_query = g.db.execute("SELECT * FROM quizzes")

        student_res = student_quuery.fetchall()
        quiz_res = quiz_query.fetchall()
        # if len(student_res) < 1 or len(quiz_res) < 1:
        #         g.db.execute("INSERT INTO students VALUES (1, 'King', 'Bach');")
        #         g.db.execute("INSERT INTO students VALUES (2, 'Serena', 'Williams');")
        #         g.db.execute("INSERT INTO students VALUES (3, 'Stephy', 'Graft');")
        #         g.db.execute("INSERT INTO students VALUES (4, 'Terron', 'Johnson');")
        #         g.db.execute("INSERT INTO students VALUES (5, 'Jack', 'Black');")
        #         g.db.execute("INSERT INTO students VALUES (6, 'Wu', 'Tang');")

        #         g.db.execute("INSERT INTO quizzes (quiz_subject, num_questions, quiz_date) VALUES ('Intro to Algorithims', 19, '2021-05-05');")
        #         g.db.execute("INSERT INTO results (quiz_id, student_id, score) VALUES (1, 1, 85);")
        #         g.db.execute("INSERT INTO results (quiz_id, student_id,  score) VALUES (1, 2, 85);")
        #         g.db.execute("INSERT INTO results (quiz_id, student_id, score) VALUES (1, 3, 85);")
        #         g.db.execute("INSERT INTO results (quiz_id, student_id, score) VALUES (1, 4, 85);")
        #         g.db.execute("INSERT INTO results (quiz_id, student_id, score) VALUES (1, 5, 85);")
        #         g.db.execute("INSERT INTO results (quiz_id, student_id, score) VALUES (1, 6, 85);")
            

        s  = []
        q = []

        for i in student_res:
            s.append({"student_id":i[0], "f_name": i[1], "l_name":i[2]})

        for i in quiz_res:
            s.append({"quiz_id":i[0], "sub": i[2], "num_que":i[2], "date":i[3]})

        return render_template('dashboard.html', students=s, quizzes=q)
    else:
        return redirect('/login')

@app.route('/student/add', methods=['GET','POST'])
def add_student():
    if session['username']=='admin':
        if request.method == 'GET':
            return render_template('add_student.html')
        elif request.method == 'POST':
            try:
                g.db.execute("INSERT into students (first_name,last_name) values (?,?)", [request.form['first_name'],request.form['last_name']])
                g.db.commit()
                return redirect('/dashboard')
            except Exception as e:
                return render_template('add_student.html')
    else:
        return redirect('/login')

@app.route('/student/<id>')
def get_results(id):

    cur = g.db.execute("SELECT * FROM students JOIN results ON students.student_id = results.student_id JOIN quizzes ON results.quiz_id = quizzes.quiz_id WHERE students.student_id = ?",[id])
    res = cur.fetchall()

    results = [dict(quiz_id=r[0], score=r[1], q_date=r[2],quiz_subject=r[3]) for r in res]

    return render_template('student_results.html', results=results)

@app.route('/results/add', methods=['GET','POST'])
def add_results():
    if session['username']=='admin':
        try:
            if request.method == 'GET':
                cur = g.db.execute("SELECT first_name,student_id FROM students")
                res = cur.fetchall()
                students = [dict(first_name=r[0],student_id=r[1]) for r in res]

                cur2 = g.db.execute("SELECT quiz_id FROM quizzes")
                res2 = cur2.fetchall()
                quizzes = [dict(quiz_id=r[0]) for r in res2]

                return render_template('add_results.html', students=students,quizzes=quizzes)

            elif request.method == 'POST':
                g.db.execute("INSERT into results (student_id,quiz_id,score) values (?,?,?)", [request.form['student'],request.form['quiz'],request.form['score']])
                g.db.commit()
                return redirect('/dashboard')

        except Exception as e:
            print(e)
            return redirect('/results/add')

@app.route('/quiz/add', methods=['GET','POST'])
def add_quiz():
    if session['username']=='admin':
        if request.method == 'GET':
            return render_template('add_quiz.html')
        elif request.method == 'POST':
            try:
                g.db.execute("INSERT into quizzes (quiz_subject,num_questions,q_date) values (?,?,?)", [request.form['quiz_subject'], request.form['num_questions'], request.form['q_date']])
                g.db.commit()
                return redirect('/dashboard')
            except Exception as e:
                print(e)
                return render_template('add_quiz.html')
    else:
        return redirect('/login')

if __name__=='__main__':
    app.debug = True
    app.run(host = '0.0.0.0', port=5001)