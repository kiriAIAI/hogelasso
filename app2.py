from flask import Flask, render_template, send_from_directory, request, redirect, url_for
import mysql.connector
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo
from flask_mail import Mail, Message  # 导入Flask-Mail
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__, template_folder='kakikko')
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['MAIL_SERVER'] = 'smtp.gmail.com'  # 邮件服务器
app.config['MAIL_PORT'] = 587  # 邮件服务器端口
app.config['MAIL_USE_TLS'] = True  # 启用TLS
app.config['MAIL_USERNAME'] = 'your_email@gmail.com'  # 你的邮件地址
app.config['MAIL_PASSWORD'] = 'your_email_password'  # 你的邮件密码
db = SQLAlchemy(app)
mail = Mail(app)  # 初始化Flask-Mail
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

def conn_db():
    conn = mysql.connector.connect(
        host="127.0.0.1", 
        user="root", 
        password="root", 
        db="hew",
        charset='utf8'
    )
    return conn
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)  # 确保传递了两个参数：存储的哈希密码和用户输入的密码

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')
@app.route('/signup.html', methods=['GET', 'POST'])
def signup():
    form = RegistrationForm()
    if form.validate_on_submit():
        existing_user = User.query.filter((User.username == form.username.data) | (User.email == form.email.data)).first()
        if existing_user:
            error_message = "Username or email already exists."
            return render_template('signup.html', form=form, error_message=error_message)

        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()

        msg = Message('Registration Successful',
                      sender='your_email@gmail.com',
                      recipients=[form.email.data])
        msg.body = 'Thank you for registering!'
        mail.send(msg)

        return redirect(url_for('signupsecurityquestion'))
    return render_template('signup.html', form=form)
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

@app.route('/login.html', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):  # 确保传递了正确的参数
            login_user(user)
            return redirect(url_for('index'))
        else:
            error_message = "Invalid username or password."
            return render_template('login.html', form=form, error_message=error_message)
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/signupsecurityquestion.html', methods=['GET', 'POST'])
def signupsecurityquestion():
    if request.method == 'POST':
        question1 = request.form.get('question-1')
        answer1 = request.form.get('answer-1')
        question2 = request.form.get('question-2')
        answer2 = request.form.get('answer-2')

        # 在这里处理秘密问题和答案，例如保存到数据库

        return redirect(url_for('signup_success'))
    return render_template('signup-security-question.html')
@app.route('/signup_success')
def signup_success():
    return "Registration successful!"

@app.route('/')
@app.route('/index.html')
def index():
    return render_template('index.html')

@app.route('/create.html')
def create():
    return render_template('create.html')

@app.route('/chatroom.html')
def chatroom():
    return render_template('chatroom.html')

@app.route('/chat.html')
def chat():
    return render_template('chat.html')

@app.route('/chatbot.html')
def chatbot():
    return render_template('chatbot.html')



@app.route('/forget-password.html')
def forgetpassword():
    return render_template('forget-password.html')

@app.route('/confirm-logout.html')
def confirmlogout():
    return render_template('confirm-logout.html')

@app.route('/notification.html')
def notification():
    return render_template('notification.html')

@app.route('/filter.html')
def filter():
    return render_template('filter.html')

@app.route('/product-details.html')
def productdetails():
    return render_template('product-details.html')

@app.route('/search.html')
def search():
    return render_template('search.html')

@app.route('/shopping-cart.html')
def shoppingcart():
    return render_template('shopping-cart.html')

@app.route('/payment.html')
def payment():
    return render_template('payment.html')

@app.route('/payment-info.html')
def paymentinfo():
    return render_template('payment-info.html')

@app.route('/payment-success.html')
def paymentsuccess():
    return render_template('payment-success.html')

@app.route('/profile.html')
def profile():
    return render_template('profile.html')

@app.route('/purchase-history.html')
def purchase_history():
    return render_template('purchase-history.html')

@app.route('/read.html')
def read():
    return render_template('read.html')

@app.route('/quiz.html')
def quiz():
    conn = conn_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT question_text, option1, option2, option3, option4 FROM questions ORDER BY RAND() LIMIT 1")
    question = cursor.fetchone()
    cursor.close()
    conn.close()
    
    if question is None:
        question = {
            'question_text': 'No question available',
            'option1': 'Option 1',
            'option2': 'Option 2',
            'option3': 'Option 3'
        }
    
    return render_template('quiz.html', question=question)
@app.route('/static/css/<path:filename>')
def css(filename):
    return send_from_directory('kakikko/static/css', filename)

@app.route('/static/js/<path:filename>')
def js(filename):
    return send_from_directory('kakikko/static/js', filename)

@app.route('/static/fonts/<path:filename>')
def fonts(filename):
    return send_from_directory('kakikko/static/fonts', filename)

@app.route('/static/images/<path:filename>')
def images(filename):
    return send_from_directory('kakikko/static/images', filename)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)








