from flask import Flask, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
import json

app = Flask(__name__)

HOSTNAME = '127.0.0.1'
PORT = 3306
USERNAME = 'root'
PASSWORD = 'qazplm820252'
DATABASE = 'OJ'
app.config['SQLALCHEMY_DATABASE_URI']=f"mysql+pymysql://{USERNAME}:{PASSWORD}@{HOSTNAME}:{PORT}/{DATABASE}?charset=utf8"
app.secret_key = 'xihwidfw9efw'
db = SQLAlchemy(app)

@app.route('/')
def index():  # put application's code here
    res = db.session.execute(text('select * from problem'))
    result = res.fetchall()
    db.session.close()  #
    return render_template('index.html', results=result)

@app.route('/reg')
def reg():
    return render_template('reg.html')

@app.route('/user_reg', methods=['GET', 'POST'])
def user_reg():
    username = request.form['Username']
    password = request.form['inputPassword']
    db.session.execute(text('insert into user(username, password) values("{}", "{}")'.format(username, password)))
    db.session.commit()
    return redirect('/')

@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')

@app.route('/user_login', methods=['GET', 'POST'])
def user_login():
    username = request.form['Username']
    password = request.form['inputPassword']
    res = db.session.execute(text('select password from user where username="{}"'.format(username)))
    result = res.fetchone()
    db.session.close()  #
    if len(result) == 0 or result[0] != password:
        return "密码错误"
    else:
        session['username'] = username
        return render_template('index.html')

@app.route('/problem_detail/<int:pid>', methods=['GET', 'POST'])
def problem_detail(pid):
    res = db.session.execute(text('select * from problem where pid="{}"'.format(pid)))
    result = res.fetchone()
    print(result.example)
    problem_example = json.loads(result.example)
    tips = json.loads(result.tips)
    return render_template('problem_detail.html', problem=result, problem_example=problem_example, tips=tips)
if __name__ == '__main__':
    app.run()
