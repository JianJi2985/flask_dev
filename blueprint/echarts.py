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
from models import echartdata, db
from sqlalchemy import desc
import json
from sqlalchemy.ext.declarative import DeclarativeMeta
from flask_cors import CORS,cross_origin

class AlchemyEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj.__class__, DeclarativeMeta):
            # an SQLAlchemy class
            fields = {}
            for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata']:
                data = obj.__getattribute__(field)
                try:
                    json.dumps(data) # this will fail on non-encodable values, like other classes
                    fields[field] = data
                except TypeError:
                    # fields[field] = None
                    fields[field]=str(data)
            # a json-encodable dict
            return fields

        return json.JSONEncoder.default(self, obj)

bp = Blueprint('echarts', __name__)

# # @bp.route('', strict_slashes=False,methods=['GET','POST'])
class EchartsView(MethodView):
    def get(self):
        builder = echartdata.query
        print('year:', request.args['year'])
        result = builder.filter_by(year=request.args['year']).all()
        return json.dumps(builder.filter_by(year=request.args['year']).all(), cls=AlchemyEncoder)
#
todo_api = EchartsView.as_view('echarts')
bp.add_url_rule('/', view_func=todo_api, methods=['GET', 'POST'],strict_slashes=True)
# # bp.add_url_rule('/<int:todo_id>', view_func=todo_api, methods=['PUT', 'DELETE'])
