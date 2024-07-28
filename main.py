from flask import Flask, request, make_response, redirect, render_template, session, url_for, flash
from flask_bootstrap import Bootstrap
from app.forms import TodoForm, DeleteTodoForm, UpdateTodoForm
import unittest
from app.firestore_service import get_users, get_todos, put_todo, delete_todo, update_todo
from app import create_app
from flask_login import login_required, current_user

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

@app.route('/hello', methods = ['GET','POST'])
@login_required
def hello():
    #user_ip = request.cookies.get('user_ip')
    #login_form = LoginForm()
    user_ip =  session.get('user_ip')
    username = current_user.id
    todo_form = TodoForm()
    delete_form = DeleteTodoForm()
    update_form = UpdateTodoForm()

    #username = session.get('username')
    context = {'user_ip':user_ip,
               'todos':get_todos(user_id=username),
              # 'login_form':login_form,
               'username': username,
               'todo_form': todo_form,
               'delete_form':delete_form,
               'update_form': update_form
    }

    if todo_form.validate_on_submit():
        put_todo(user_id=username,description=todo_form.description.data)
        flash('Activity was created successfully')
        return redirect(url_for('hello'))

    # users = get_users()
    # for user in users:
    #     print(user.id)
    #     print(user.to_dict()['password'])

    # if login_form.validate_on_submit():
    #     username = login_form.username.data
    #     session['username'] = username
    #     flash('Username successfully')
    #     return redirect(url_for('index'))

    return render_template('hello.html',**context) # ** expand the dictionary

    #return "Hello world Flask, your IP is {}".format(user_ip)

@app.route('/todos/delete/<todo_id>', methods=['POST'])
def delete(todo_id):
    user_id = current_user.id
    delete_todo(user_id=user_id, todo_id=todo_id)

    return redirect(url_for('hello'))

@app.route('/todos/update/<todo_id>/<int:done>', methods=['POST'])
def update(todo_id, done):
    user_id = current_user.id
    update_todo(user_id=user_id, todo_id=todo_id,done=done)
    
    return redirect(url_for('hello'))

