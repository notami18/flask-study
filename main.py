from flask import Flask, request, redirect, make_response, render_template, session, url_for, flash
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired

app: Flask = Flask(__name__)
bootstrap = Bootstrap(app)

app.config['SECRET_KEY'] = 'Super-secret-key'

todos: list[str] = ["Comprar cafe", "Enviar solicitud de compra", "Producir un mensaje"]

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    sumit = SubmitField('Sumit')

@app.errorhandler(404)
def page_not_found(error: Exception):
    return render_template('404.html', error=error)

@app.errorhandler(500)
def internal_server_error():
    return render_template('500.html')

@app.route('/')
def index():
    user_ip = request.remote_addr
    response = make_response(redirect('/hello'))
    session['user_ip'] = user_ip

    return response


@app.route('/hello', methods=['GET', 'POST'])
def hello():
    user_ip = session.get('user_ip')
    login_form = LoginForm()
    username = session.get('username')

    context = {
        'user_ip': user_ip,
        'todos': todos,
        'login_form': login_form,
        'username': username
    }
    if login_form.validate_on_submit():
        username = login_form.username.data
        session['username'] = username
        flash('Logged in successfully!')
        return redirect(url_for('index'))

    return render_template('hello.html', **context)
