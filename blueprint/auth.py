from flask import Blueprint,Flask, request, jsonify, redirect, url_for, render_template, flash
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
from flask_apscheduler import APScheduler
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import DataRequired, EqualTo, ValidationError, Length
from time import sleep
from datetime import datetime
from flask_socketio import SocketIO
import tushare as ts
from models import User, db,Profile

bp = Blueprint('auth', __name__)

class LoginForm(FlaskForm):
    userName = StringField('userName', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    autoLogin = BooleanField('autoLogin')

    def __init__(self, *args, **kwargs):
        kwargs['csrf_enabled'] = False
        super(LoginForm, self).__init__(*args, **kwargs)

    def get_user(self):
        print("here is print")
        print(self.userName.data,self.password.raw_data,self.autoLogin.data)
        # print(User.query.filter_by)
        return User.query.filter_by(username=self.userName.data).first()

    def validate_userName(self, field):
        if not self.get_user():
            raise ValidationError('Invalid username!')

    def validate_password(self, field):
        if not self.get_user():
            return
        if not self.get_user().verify_password(field.data):
            raise ValidationError('Incorrect password!')

class RegisterForm(FlaskForm):

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

@bp.route('/login', methods=['POST'])
def login():
    user_data = request.get_json()
    form = LoginForm(data=user_data)
    if form.validate():
        user = form.get_user()
        login_user(user, remember=form.autoLogin.data)
        return jsonify({'status': 'ok','type':'account','currentAuthority': user.authority})
    return jsonify({'status': 'error','type':'account', })

@bp.route('/currentUser', methods=['GET'])
def getCurrentUser():
    curr_user_id = current_user.get_id()
    curr_user_profile=Profile.query.filter_by(id=curr_user_id).first()
    if curr_user_profile:
        name=curr_user_profile.name
        avatar=curr_user_profile.avatar
        userid=curr_user_profile.userid
        email=curr_user_profile.email
        phone=curr_user_profile.phone
        return jsonify({'name': name,'avatar':avatar,'userid':userid,'email':email,'phone':phone})
    return jsonify({'status': 'fail'}), 400

# @bp.route('/register', methods=['GET', 'POST'])
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


@bp.route('/logout',methods=['GET'])
def logout():
    logout_user()
    return jsonify({'status': 'success'})