from os import environ

SQLALCHEMY_DATABASE_URI = environ.get("DATABASE_URI", "postgresql+psycopg2://localhost/mame")
STATIC_URL = "http://mame.kageurufu.net/"
del environ