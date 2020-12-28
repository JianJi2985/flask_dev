from flask import Blueprint, Flask, request, jsonify, redirect, url_for, render_template, flash
from flask.helpers import make_response
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
from flask import send_file, make_response
import time
from mail import send_html_mail, send_plain_mail

bp = Blueprint('excel', __name__)
CORS(bp, methods=['GET', 'POST'])

class ExcelView(MethodView):
    # def parse(self,args):
    #     parseres=jsonify(args)
    #     for k,v in parseres.items():
    #         if k=='ISSUESIZE':
    #             parseres[k]=
    def get(self):
        result = Bond.query.all()
        name = uuid.uuid1().__str__() + ".csv"
        html = "<table>"
        with open(name, "w") as fd:
            fd.write("债券名称,债券描述,发行规模（亿）,票面利率,债券类型,发行日期,到期日期\n")
            html += "<tr><th>SECUABBR</th><th>CHINAME</th><th>ISSUESIZE</th><th>COUPONRATE</th><th>SECUCATEGORY</th><th>LISTINGDATE</th><th>DELISTINGDATE</th></tr>"
            for row in result:
                fd.write('{},{},{},{},{},{},{}\n'.format(
                    row.SECUABBR, row.CHINAME, row.ISSUESIZE, row.COUPONRATE, row.SECUCATEGORY, row.LISTINGDATE,
                    row.DELISTINGDATE))
                html += "<tr><th>{}</th><th>{}</th><th>{}</th><th>{}</th><th>{}</th><th>{}</th><th>{}</th></tr>".format(
                    row.SECUABBR, row.CHINAME, row.ISSUESIZE, row.COUPONRATE, row.SECUCATEGORY, row.LISTINGDATE,
                    row.DELISTINGDATE)
        html += "</table>"
        # 发送邮件
        try:
            send_html_mail("alpaca233666@gmail.com", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + "债券数据", html)
        except Exception as e:
            print("Cannot send mail: ", e.with_traceback())
        response = make_response(send_file(name, as_attachment=True))
        response.headers["content-disposition"] = "attachment; filename=" + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + ".csv"
        return response 


todo_api = ExcelView.as_view('bond')
bp.add_url_rule('/', view_func=todo_api, methods=['GET', 'POST', 'DELETE'], strict_slashes=True)