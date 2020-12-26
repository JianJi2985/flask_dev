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
CORS(bp,methods=['GET','POST'])

# # @bp.route('', strict_slashes=False,methods=['GET','POST'])
class EchartsView(MethodView):
    def get(self):
        print('request.args')
        print(request.args)

        return request.args
#     # def to_json(self):
#     #     return {k: getattr(self, k) for k in ('id', 'text', 'done')}
#
#     def post(self):
#         print("post args")
#         print(request.get_json())
#         args=request.get_json()
#         initargs={}
#         for key in args:
#             if hasattr(Bond, key):
#                 initargs[key]=args[key]
#         id=Bond.query.count()+1
#         newbond = Bond(id=id,**initargs)
#         # newbond.user = current_user
#         db.session.add(newbond)
#         db.session.commit()
#         return jsonify(newbond.to_json())
#
#     # def put(self, todo_id):
#     #     todo = Todo.query.get_or_404(todo_id)
#     #     data = request.get_json()
#     #     for k, v in data.items():
#     #         setattr(todo, k, v)
#     #     db.session.commit()
#     #     return jsonify({'status': 'success', 'todo': todo.to_json()})
#     #
#     # def delete(self, todo_id):
#     #     todo = Bond.query.get_or_404(todo_id)
#     #     db.session.delete(todo)
#     #     db.session.commit()
#     #     return jsonify({'status': 'success'})
#
#
todo_api = EchartsView.as_view('echarts')
bp.add_url_rule('/', view_func=todo_api, methods=['GET', 'POST'],strict_slashes=True)
# # bp.add_url_rule('/<int:todo_id>', view_func=todo_api, methods=['PUT', 'DELETE'])
