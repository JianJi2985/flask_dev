from flask import Flask, request, jsonify, redirect, url_for, render_template, flash
from flask_script import Manager, Shell
from flask.views import MethodView
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
from time import sleep

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

    def __init__(self, *args, **kwargs):
        kwargs['csrf_enabled'] = False
        super(RegisterForm, self).__init__(*args, **kwargs)

    username = StringField('Username', validators=[Length(max=64)])
    password = PasswordField('Password', validators=[Length(8, 16)])
    confirm = PasswordField('Confirm Password')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).count() > 0:
            raise ValidationError('Username %s already exists!' % field.data)

    def validate_password(self, field):
        if self.password != self.confirm:
            raise ValidationError('Password inconsistency!')


class LoginForm(FlaskForm):
    """登录表单类"""
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        kwargs['csrf_enabled'] = False
        super(LoginForm, self).__init__(*args, **kwargs)

    def get_user(self):
        return User.query.filter_by(username=self.username.data).first()

    def validate_username(self, field):
        if not self.get_user():
            raise ValidationError('Invalid username!')

    def validate_password(self, field):
        if not self.get_user():
            return
        if not self.get_user().verify_password(field.data):
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


@app.route('/register', methods=['GET', 'POST'])
def register():
    user_data = request.get_json()
    form = RegisterForm(data=user_data)
    if form.validate():
        user = User(username=user_data['username'], password=user_data['password'])
        print(user.id)
        db.session.add(user)
        db.session.commit()
        return jsonify({'status': 'success'})
    return jsonify({'status': 'fail', 'errormsg': form.errors}), 400


@app.route('/login', methods=['POST', 'GET'])
def login():
    user_data = request.get_json()
    form = LoginForm(data=user_data)

    emsg = None
    if form.validate():
        user = form.get_user()
        print(user.password)
        print(user.username)
        login_user(user)  # 创建用户 Session
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

@app.route('/long-polling')
def long_polling():
    i = 0
    while True:
        if i == 10:
            return jsonify({'error': 0,'msg':'未查询到更新'})
        else:
            i += 1
            sleep(5)
# CREATE TABLE Trade (
#     ID int NOT NULL,
#     product varchar(50) NOT NULL,
#     volumn float not null,
#     timestamp date,
#     is_valid boolean,
#     PRIMARY KEY (ID)
# );
# insert into trade value(1,'A',5.4,'2020-01-02',True);
class Trade(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    product = db.Column(db.String(50),nullable=False)
    volumn = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)
    is_valid = db.Column(db.Boolean, nullable=False)

    def __init__(self, **kwargs):
        super(Trade, self).__init__(**kwargs)

class TradeAPI(MethodView):

    def get(self):
        trade=request.get_json()
        if ('start_date' not in trade) or (not trade['start_date']):
            start_date='2000-01-01'
        if ('end_date' not in trade) or (not trade['end_date']):
            end_date='2020-12-31'

        result=db.session.query('Trade').filter(Trade.timestamp.between(start_date, end_date)).all()
        return jsonify(result)

    def post(self):
        trade = request.get_json()
        new_trade= Trade(trade)
        db.session.add(new_trade)
        db.session.commit()
        return jsonify({'status':'success'})


    # @login_required # need to implement
    # @admin_required
    def delete(self):
        id=request.get_json()['id']
        Trade.query.filter_by(id=id).delete()
        db.commit()
        return jsonify({'status':'success'})


    def put(self):
        trade = request.get_json()
        current_trade=Trade.query.get(trade['id'])
        current_trade.product=trade['product']
        current_trade.volumn=trade['volumn']
        current_trade.timestamp = trade['timestamp']
        current_trade.is_valid = trade['is_valid']
        db.session.commit()
        return jsonify({'status':'success'})

trade_view = TradeAPI.as_view('trade_api')
app.add_url_rule('/trade/',view_func=trade_view, methods=['GET','POST','PUT','DELETE'])


if __name__ == '__main__':
    # with app.app_context():
    #     db.create_all()
    # csrf = CSRFProtect()
    # csrf.init_app(app)
    # print(app.config['WTF_CSRF_CHECK_DEFAULT'])
    # app.config['WTF_CSRF_CHECK_DEFAULT'] = False
    # print(app.config['WTF_CSRF_CHECK_DEFAULT'])
    app.run()
