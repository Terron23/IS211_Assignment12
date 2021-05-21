import sqlite3
from flask import Flask, request, session, g, redirect, url_for, render_template, flask
import datetime
app = Flask(__name__)


def connect_db():
    db = sqlite3.connect('homework.db')
    db.row_factory = sqlite3.Row
    return db

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

        s  = []
        q = []

        for i in student_res:
            s.append({"s_id":i[0], "f_name": i[2], "l_name":i[3]})

        for i in quiz_res:
            s.append({"q_id":i[0], "sub": i[2], "num_que":i[2], "date":i[3]})

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

    cur = g.db.execute("SELECT * FROM students JOIN results ON students.s_id = results.s_id JOIN quizzes ON results.q_id = quizzes.q_id WHERE students.s_id = ?",[id])
    res = cur.fetchall()

    results = [dict(q_id=r[0], score=r[1], q_date=r[2],q_subject=r[3]) for r in res]

    return render_template('student_results.html', results=results)

@app.route('/results/add', methods=['GET','POST'])
def add_results():
    if session['username']=='admin':
        try:
            if request.method == 'GET':
                cur = g.db.execute("SELECT first_name,s_id FROM students")
                res = cur.fetchall()
                students = [dict(first_name=r[0],s_id=r[1]) for r in res]

                cur2 = g.db.execute("SELECT q_id FROM quizzes")
                res2 = cur2.fetchall()
                quizzes = [dict(q_id=r[0]) for r in res2]

                return render_template('add_results.html', students=students,quizzes=quizzes)

            elif request.method == 'POST':
                g.db.execute("INSERT into results (s_id,q_id,score) values (?,?,?)", [request.form['student'],request.form['quiz'],request.form['score']])
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
                g.db.execute("INSERT into quizzes (q_subject,num_questions,q_date) values (?,?,?)", [request.form['q_subject'], request.form['num_questions'], request.form['q_date']])
                g.db.commit()
                return redirect('/dashboard')
            except Exception as e:
                print(e)
                return render_template('add_quiz.html')
    else:
        return redirect('/login')

if __name__=='__main__':
    app.debug = True
    app.run(host = '0.0.0.0', port=5000)