__author__ = 'frank'
from .. import app, db, models, render_template, url_for, redirect, abort, request

@app.route("/game")
def gameindex():
    letter = None
    page = int(request.args.get("page", 1))
    if request.args.get("letter"):
        letter = request.args['letter']
    if letter == "#":
        query = models.Game.query.filter(models.Game.name.op("SIMILAR TO")("[0-9]%"))
    elif letter:
        query = models.Game.query.filter(models.Game.name.startswith(letter.lower()))
    else:
        query = models.Game.query
    games = query.paginate(page=page, per_page=30)
    return render_template("gameindex.html", games=games)

@app.route("/game/<game_name>")
def game(game_name = None):
    query = models.Game.query
    game = query.filter_by(name = game_name).first_or_404()
    return render_template("game.html", game=game)

@app.route("/random")
def random():
    game = models.Game.query.with_entities(models.Game.name).order_by(db.func.random()).limit(1).first()
    return redirect("/game/%s" % game[0])