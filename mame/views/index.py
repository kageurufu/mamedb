__author__ = 'frank'

from .. import app, models, db, render_template, redirect, url_for, abort

@app.route("/")
def index():
    count = models.Game.query.count()
    random = models.Game.query.order_by(db.func.random()).limit(10).all()
    return render_template("index.html", count=count, games=random)

@app.route("/project")
def project():
    return render_template("project.html")