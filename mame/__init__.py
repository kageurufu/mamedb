__author__ = 'frank'

from flask import Flask, render_template, redirect, url_for, abort, request
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.bootstrap import Bootstrap

app = Flask(__name__)
app.config.from_pyfile("config.py")

db = SQLAlchemy(app)
Bootstrap(app)

from . import models

from . import views
