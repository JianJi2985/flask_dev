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
from flask_apscheduler import APScheduler
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import DataRequired, EqualTo, ValidationError, Length
from time import sleep
from datetime import datetime
from flask_socketio import SocketIO
import tushare as ts

db = SQLAlchemy()

class User(UserMixin, db.Model):
    """用户类"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(200), unique=True,nullable=False)
    password = db.Column(db.String(200),nullable=False)
    authority = db.Column(db.String(20),nullable=False)

    def __init__(self, **kwarg):
        kwarg['password'] = generate_password_hash(kwarg.get("password"))
        super(User, self).__init__(**kwarg)

    def verify_password(self, password):
        if self.password is None:
            return False
        return check_password_hash(self.password, password)

class Profile(db.Model):
    """用户类"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), unique=True,nullable=False)
    avatar = db.Column(db.String(200))
    userid = db.Column(db.String(20))
    email = db.Column(db.String(50))
    phone = db.Column(db.String(50))

    def __init__(self, **kwarg):
        super(Profile, self).__init__(**kwarg)


class Bond(db.Model):
    """交易类"""
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    SECUABBR = db.Column(db.String(200), unique=True,nullable=False)
    CHINAME = db.Column(db.String(200))
    SECUCATEGORY = db.Column(db.String(20))
    ISSUESIZE = db.Column(db.Integer)
    COUPONRATE = db.Column(db.Integer)
    LISTINGDATE=db.Column(db.DateTime)
    DELISTINGDATE=db.Column(db.DateTime)
    isvalid=db.Column(db.Boolean)

    def __init__(self, **kwarg):
        super(Bond, self).__init__(**kwarg)

    def to_json(self):
        return {k: getattr(self, k) for k in ('id', 'SECUABBR', 'CHINAME','SECUCATEGORY','ISSUESIZE','COUPONRATE','LISTINGDATE','DELISTINGDATE')}




class EchartData(db.Model):
    """交易类"""
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    year = db.Column(db.String(4))
    income = db.Column(db.Float)
    expense = db.Column(db.Float)
    month = db.Column(db.String(2))
    dataversion=db.Column(db.Integer)


    def __init__(self, **kwarg):
        super(EchartData, self).__init__(**kwarg)

    def to_json(self):
        return {k: getattr(self, k) for k in ('id', 'year', 'income','expense','month')}


