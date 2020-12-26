from flask import Blueprint, Flask, request, jsonify, redirect, url_for, render_template, flash
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
from models import Bond, db
from sqlalchemy import desc
import json
from sqlalchemy.ext.declarative import DeclarativeMeta
from flask_cors import CORS, cross_origin

bp = Blueprint('excel', __name__)
CORS(bp, methods=['GET', 'POST'])

class ExcelView(MethodView):
    # def parse(self,args):
    #     parseres=jsonify(args)
    #     for k,v in parseres.items():
    #         if k=='ISSUESIZE':
    #             parseres[k]=
    def get(self):
        print('request is')
        print(session)


todo_api = ExcelView.as_view('bond')
bp.add_url_rule('/', view_func=todo_api, methods=['GET', 'POST', 'DELETE'], strict_slashes=True)