__author__ = 'frank'
from .. import app, db, models, render_template

@app.errorhandler(404)
def error_404(e):
    return render_template("404.html"), 404