from flask import Flask, request, make_response, redirect, render_template, session, url_for, flash
from flask_bootstrap import Bootstrap
from app.forms import LoginForm
import unittest
from app.firestore_service import get_users, get_todos
from app import create_app

app = create_app()

todos = ['buy coffe','send request','deliver video to productor']


@app.cli.command()
def test():
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner().run(tests)


@app.errorhandler(500)
def server_internal_error(error):
    return render_template('500.html',error=error)

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html',error=error)

@app.route("/")
def index():
    user_ip= request.remote_addr    
    response = make_response(redirect('/hello'))
    session['user_ip']= user_ip    
    #response.set_cookie('user_ip',user_ip)
    return response

@app.route('/hello', methods = ['GET'])
def hello():
    #user_ip = request.cookies.get('user_ip')
    #login_form = LoginForm()
    user_ip =  session.get('user_ip')
    username = session.get('username')
    context = {'user_ip':user_ip,
               'todos':get_todos(user_id=username),
              # 'login_form':login_form,
               'username': username
    }
    users = get_users()
    for user in users:
        print(user.id)
        print(user.to_dict()['password'])

    # if login_form.validate_on_submit():
    #     username = login_form.username.data
    #     session['username'] = username
    #     flash('Username successfully')
    #     return redirect(url_for('index'))

    return render_template('hello.html',**context) # ** expand the dictionary

    #return "Hello world Flask, your IP is {}".format(user_ip)
