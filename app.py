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
import json
from flask_wtf import FlaskForm
from flask_apscheduler import APScheduler
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import DataRequired, EqualTo, ValidationError, Length
from time import sleep
from datetime import datetime
from flask_socketio import SocketIO
import tushare as ts
from models import db, User, bondflag,Bond
import os
from blueprint import auth, bonds, echarts
from flask_migrate import Migrate
from flask_cors import CORS
from flask_socketio import SocketIO
import pandas as pd

# app = Flask(__name__)
# app.secret_key = 'iashdfpi'
# app.config.update(
#     SCHEDULER_API_ENABLED=True,
#     SQLALCHEMY_DATABASE_URI='mysql+pymysql://root:1234@127.0.0.1/flask_dev',
#     SQLALCHEMY_TRACK_MODIFICATIONS=False,
#     DEBUG=True,
#     MAIL_SERVER='smtp.163.com',  # 邮箱服务器
#     MAIL_PROT=25,  # 每种邮箱服务器都有自己的端口
#     MAIL_USE_TLS=True,
#     MAIL_USE_SSL=False,
#     MAIL_USERNAME='rbs_jijian@163.com',  # 邮箱账户
#     MAIL_PASSWORD='AWGIHRBEBSVPURHA',  # 授权码
#     MAIL_DEBUG=True
# )
# app.config['JOBS'] = [{'id': 'job1',
#                        'func': '__main__:job_test',
#                        'args': (1, 2),
#                        'trigger': 'cron',  # cron表示定时任务
#                        'hour': 20,
#                        'minute': 9},
#                       # {'id': 'job2',
#                       #  'func': '__main__:interval_test',
#                       #  'trigger': 'interval',
#                       #  'seconds': 20,
#                       #  }
#                        ]
# mail = Mail(app)
# db = SQLAlchemy(app)
# login_manager = LoginManager()  # 实例化登录管理对象
# login_manager.init_app(app)  # 初始化应用
# login_manager.login_view = 'login'  # 设置用户登录视图函数 endpoint





def daily_fetch_data():
    # stock_all = ts.get_today_all()
    stock_all = ts.get_k_data(code='600000', start='2019-10-01', end='2019-10-07')
    stock_all.to_csv('./download/%s.csv' % (datetime.today().strftime('%Y%m%d')))
    filename = datetime.today().strftime('%Y%m%d')
    id = BondFlag.query.count() + 1
    newBondFlag = BondFlag(id=id, filename=filename, isvalid=True)
    db.session.add(newBondFlag)
    db.session.commit()
    print('daily_fetch_data success ')


msg = Message('test', sender='rbs_jijian@163.com', recipients=['rbs_jijian@163.com'])
msg.body = "This is a first email"


# with app.open_resource("./test_mail_attachment.txt") as fp:
#     msg.attach("test_mail_attachment.txt", "text/plain", fp.read())


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


# @app.route('/send_email')
# def send_email():
#     thread = Thread(target=send_async_email, args=[app, msg])
#     thread.start()
#     return jsonify(dict(msg="Success"))


# @app.route('/register', methods=['GET', 'POST'])
# def register():
#     user_data = request.get_json()
#     form = RegisterForm(data=user_data)
#     if form.validate():
#         user = User(username=user_data['username'], password=user_data['password'])
#         print(user.id)
#         db.session.add(user)
#         db.session.commit()
#         return jsonify({'status': 'success'})
#     return jsonify({'status': 'fail', 'errormsg': form.errors}), 400


# @app.route('/api/login/currentUser', methods=['GET'])
# def getCurrenetUser():

# @app.route('/api/login/account', methods=['POST'])
# def login():
# user_data = request.get_json()
# form = LoginForm(data=user_data)
#
# emsg = None
# if form.validate():
#     user = form.get_user()
#     print(user.password)
#     print(user.username)
#     login_user(user)  # 创建用户 Session
#     # return redirect(request.args.get('next') or url_for('index'))
#     return jsonify({'status': 'success'})
# # return render_template('login.html', form=form, emsg=emsg)
# return jsonify({'status': 'ok','type': 'account','currentAuthority':'admin'})


# @app.route('/logout')  # 登出
# @login_required
# def logout():
#     logout_user()
#     return redirect(url_for('login'))
#
#
# @app.route('/long-polling')
# def long_polling():
#     i = 0
#     while True:
#         if i == 10:
#             return jsonify({'error': 0, 'msg': '未查询到更新'})
#         else:
#             i += 1
#             sleep(5)
def interval_test():
    print('interval_test')
    with app.app_context():
        validfiles=bondflag.query.filter_by(isvalid=True).all()
        for file in validfiles:
            print('validfiles is')
            print(file.filename)
            path='./download/%s' % file.filename
            print('path is')
            print(path)
            df=pd.read_csv(path)
            df['json'] = df.apply(lambda x: x.to_json(), axis=1)
            for val in df['json'].values:
                args=json.loads(val)
                initargs = {}
                for key in args:
                    if hasattr(Bond, key):
                        initargs[key] = args[key]
                id = Bond.query.count() + 1
                newbond = Bond(id=id, isvalid=True, **initargs)
                # newbond.user = current_user
                db.session.add(newbond)
                db.session.commit()
            file.isvalid=False
            db.session.commit()


def create_app():

    app = Flask(__name__)

    app.secret_key = 'iashdfpi'
    app.config.update(
        SCHEDULER_API_ENABLED=True,
        SQLALCHEMY_ECHO=True,
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
    app.config['JOBS'] = [{'id': 'job1',
                           'func': '__main__:daily_fetch_data',
                           # 'args': (1, 2),
                           'trigger': 'cron',  # cron表示定时任务
                           'hour': 20,
                           'minute': 9},
                          {'id': 'job2',
                           'func': '__main__:interval_test',
                           'trigger': 'interval',
                           'seconds': 5,
                           }
                          ]
    mail = Mail(app)
    db.init_app(app)
    # CSRFProtect(app)
    Migrate(app, db)
    # db.drop_all()
    # db.drop_all()

    CORS(app, resources={r"/*": {"origins": "*"}})
    # cors=CORS(app,support_credentials=True,resources=r'/*')
    # cors = CORS(app,  methods=['GET', 'HEAD', 'POST', 'OPTIONS'])

    login_manager = LoginManager()  # 实例化登录管理对象
    login_manager.init_app(app)  # 初始化应用
    login_manager.login_view = '/login'  # 设置用户登录视图函数 endpoint
    scheduler = APScheduler()
    scheduler.init_app(app)
    scheduler.start()

    # socketio = SocketIO(app, cors_allowed_origins='*')

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

    @app.route('/')  # 首页
    @login_required  # 需要登录才能访问
    def index():
        return render_template('index.html')

    app.register_blueprint(auth.bp, url_prefix="/auth")
    app.register_blueprint(bonds.bp, url_prefix="/rule")
    app.register_blueprint(echarts.bp, url_prefix="/echarts")

    return app


if __name__ == '__main__':
    # with app.app_context():
    #     db.create_all()
    # csrf = CSRFProtect()
    # csrf.init_app(app)
    # print(app.config['WTF_CSRF_CHECK_DEFAULT'])
    # app.config['WTF_CSRF_CHECK_DEFAULT'] = False
    # print(app.config['WTF_CSRF_CHECK_DEFAULT'])
    app = create_app()
    app.run(host='0.0.0.0')
