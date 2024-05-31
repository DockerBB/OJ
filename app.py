import datetime
from dataclasses import asdict

from flask import Flask, render_template, request, redirect, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
import json
import requests

app = Flask(__name__)

HOSTNAME = '127.0.0.1'
PORT = 3306
USERNAME = 'root'
PASSWORD = 'qazplm820252'
DATABASE = 'OJ'
app.config[
    'SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{USERNAME}:{PASSWORD}@{HOSTNAME}:{PORT}/{DATABASE}?charset=utf8"
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


@app.route('/submit_problem/<int:pid>', methods=['POST'])
def submit_problem(pid):
    # 获取客户端提交的表单数据
    form_data = request.form.to_dict()
    # print(form_data)
    response = requests.post(f'http://127.0.0.1:8000/problems/{pid}/judge', data=json.dumps(form_data),
                             headers={'Content-Type': 'application/json'})

    if response.status_code == 200:
        # 返回另一个 API 的响应
        print(response.json())
        return jsonify(response.json())
    else:
        # 返回错误信息
        return jsonify({'error': 'Failed to send data to other API'}), 500


@app.route('/problem_manage', methods=['GET', 'POST'])
def problem_manage():
    res = db.session.execute(text('select * from problem'))
    # for item in res:
    #     print(item)
    results = [dict(row_proxy._mapping) for row_proxy in res]
    # json_data = jsonify(results)

    if request.method == 'POST':
        pass
    return render_template('problem_manage.html', results=results)


@app.route('/testcase_manage', methods=['GET', 'POST'])
def testcase_manage():
    return "用例管理页面"


@app.route('/update_problem/<int:pid>', methods=['POST'])
def update_problem(pid):
    data = request.json
    try:
        res = db.session.execute(text('''
            UPDATE problem
            SET title = :title, content = :content, tips = :tips, difficulty = :difficulty
            WHERE pid = :pid
        '''), {'title': data['title'], 'content': data['content'], 'tips': json.dumps(data['tips']),
               'difficulty': data['difficulty'], 'pid': data['pid']})

        db.session.commit()  # 提交事务

        return jsonify({'success': True, 'message': '更新成功!'})
    except Exception as e:
        db.session.rollback()  # 回滚事务
        return jsonify({'success': False, 'message': str(e)})


@app.route('/add_problem', methods=['POST'])
def add_problem():
    data = request.json
    try:
        res = db.session.execute(text('''
            insert into problem(title, content, tips, difficulty)
            values(:title, :content, :tips, :difficulty)
        '''), {'title': data['title'], 'content': data['content'], 'tips': json.dumps(data['tips']),
               'difficulty': data['difficulty']})

        db.session.commit()  # 提交事务

        return jsonify({'success': True, 'message': '插入成功!'})
    except Exception as e:
        db.session.rollback()  # 回滚事务
        return jsonify({'success': False, 'message': str(e)})


@app.route('/delete_problem/<int:pid>', methods=['GET'])
def delete_problem(pid):
    try:
        res = db.session.execute(text('''
            delete from problem
            where pid = :pid
        '''), {'pid': pid})

        db.session.commit()  # 提交事务

        return jsonify({'success': True, 'message': '删除成功!'})
    except Exception as e:
        db.session.rollback()  # 回滚事务
        return jsonify({'success': False, 'message': str(e)})

if __name__ == '__main__':
    app.run(port=8899)
