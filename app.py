from flask import Flask, request, jsonify, redirect, url_for, render_template
from flask_script import Manager, Shell
from flask_mail import Mail, Message
from threading import Thread
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, current_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf.csrf import CSRFProtect
import uuid
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import DataRequired, EqualTo, ValidationError, Length

import os

app = Flask(__name__)
app.secret_key = 'iashdfpi'
app.config.update(
    SQLALCHEMY_DATABASE_URI='mysql+pymysql://root:1234@127.0.0.1/flask_dev',
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
    DEBUG=True,
    MAIL_SERVER='smtp.163.com',  # 邮箱服务器
    MAIL_PROT=25,  # 每种邮箱服务器都有自己的端口
    MAIL_USE_TLS=True,
    MAIL_USE_SSL=False,
    MAIL_USERNAME='rbs_jijian@163.com',  # 邮箱账户
    MAIL_PASSWORD='AWGIHRBEBSVPURHA',  # 授权码
    MAIL_DEBUG=True
)
mail = Mail(app)
db = SQLAlchemy(app)
login_manager = LoginManager()  # 实例化登录管理对象
login_manager.init_app(app)  # 初始化应用
login_manager.login_view = 'login'  # 设置用户登录视图函数 endpoint

#     =False,

class RegisterForm(FlaskForm):
    """注册表单类"""
    username = StringField('Username', validators=[Length(max=64)])
    password = PasswordField('Password', validators=[Length(8, 16)])
    confirm = PasswordField('Confirm Password')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).count() > 0:
            raise ValidationError('Username %s already exists!' % field.data)


class LoginForm(FlaskForm):
    """登录表单类"""
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])

    def get_user(self):
        return User.query.filter_by(username=self.username.data).first()

    def validate_username(self, field):
        if not self.get_user():
            raise ValidationError('Invalid username!')

    def validate_password(self, field):
        if not self.get_user():
            return
        if not self.get_user().verify_password(field.data):
            print(field.data)
            print(self.get_user().password)
            raise ValidationError('Incorrect password!')



class User(UserMixin, db.Model):
    """用户类"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(200), unique=True)
    password = db.Column(db.String(200))

    def __init__(self, **kwarg):
        kwarg['password'] = generate_password_hash(kwarg.get("password"))
        super(User, self).__init__(**kwarg)

    def verify_password(self, password):
        """密码验证"""
        # print("verity here ", self.password)
        if self.password is None:
            return False
        return check_password_hash(self.password, password)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


msg = Message('test', sender='rbs_jijian@163.com', recipients=['rbs_jijian@163.com'])
msg.body = "This is a first email"
with app.open_resource("./全国天气数据.txt") as fp:
    msg.attach("全国天气数据.txt", "text/plain", fp.read())


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


@app.route('/send_email')
def send_email():
    thread = Thread(target=send_async_email, args=[app, msg])
    thread.start()
    return jsonify(dict(msg="Success"))


@app.route('/register', methods=['GET','POST'])
def register():
    user_data = request.get_json()
    form = RegisterForm(data=user_data)
    if form.validate():

        user = User(user_data['username'], user_data['password'])
        db.session.add(user)
        db.commit()
        return jsonify({'status': 'success'})
    return jsonify({'status': 'fail', 'errormsg': form.errors}), 400


@app.route('/login', methods=['POST', 'GET'])
def login():
    user_data=request.get_json()
    form = LoginForm(data=user_data)
    emsg = None
    if form.validate_on_submit():
        user = form.get_user()
        print(user.password)
        print(user.username)
        login_user(user)  # 创建用户 Session
        # print('request.args.getis',request.args.get('next'))
        return redirect(request.args.get('next') or url_for('index'))
    return render_template('login.html', form=form, emsg=emsg)


@app.route('/')  # 首页
@login_required  # 需要登录才能访问
def index():
    return render_template('index.html', username=current_user.username)


@app.route('/logout')  # 登出
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    csrf = CSRFProtect()
    csrf.init_app(app)
    print(app.config['WTF_CSRF_CHECK_DEFAULT'])
    app.config['WTF_CSRF_CHECK_DEFAULT'] = False
    print(app.config['WTF_CSRF_CHECK_DEFAULT'])
    app.run()
