from wtforms.fields.core import RadioField

__author__ = 'frank'
from .. import app, db, models, redirect, render_template, request, abort, url_for
from flask.ext.wtf import Form
from wtforms.fields import TextField, SelectField, SelectMultipleField, BooleanField, SubmitField, HiddenField
from wtforms.validators import Optional, Required, InputRequired

#values for searching go here
yesno = [(c,c) for c in ["", "yes", "no"]]
enum_status = [(c,c) for c in ["", "good", "imperfect", "preliminary"]]
enum_dump_status = [(c,c) for c in ["", "baddump", "nodump", "good"]]
enum_savestate = [(c,c) for c in ["", "supported", "unsupported"]]
years = [(c,c) for c in ["", "????", "19??", "1971", "1972", "1974", "1975", "1976", "1977", "1978", "1979", "1979?", "198?", "1980", "1980?", "1981", "1981?", "1982", "1982?", "1983", "1983?", "1984", "1984?", "1985", "1986", "1986?", "1987", "1987?", "1988", "1988?", "1989", "1989?", "199?", "1990", "1990?", "1991", "1991?", "1992", "1992?", "1993", "1993?", "1994", "1994?", "1995", "1995?", "1996", "1996?", "1997", "1998", "1999", "1999?", "200?", "2000", "2000?", "2001", "2002", "2002?", "2003", "2004", "2004?", "2005", "2005?", "2006", "2007", "2007?", "2008", "2009", "2010"]]
enum_control_type = [(c,c) for c in ["", "joy", "paddle", "gambling", "pedal", "keypad", "hanafuda", "lightgun", "trackball", "positional", "dial", "doublejoy", "mouse", "stick", "mahjong", "keyboard"]]

class SearchForm(Form):

    name = TextField("Rom Name", validators=[Optional()], default='')
    description = TextField("Description", validators=[Optional()], default='')
    manufacturer = TextField("Manufacturer", validators=[Optional()], default='')

    year = SelectField("Year", choices=years, validators=[Optional()], default='')

    type = SelectField("ROM Type", validators=[Optional()], choices=[(c,c) for c in ['All', 'Bios', 'Device', 'Mechanical']])

    cloneof = SelectField("Show Clones?", default='Yes', validators=[Optional()], choices=[('Yes', 'Yes'), ('No', 'No')])

    rom_status = SelectField("Rom Status", choices=enum_dump_status, validators=[Optional()], default='')
    
    status = SelectField("Overall Status", choices=enum_status, validators=[Optional()], default='')
    emulation = SelectField("Emulation Status", choices=enum_status, validators=[Optional()], default='')
    color = SelectField("Color Status", choices=enum_status, validators=[Optional()], default='')
    sound = SelectField("Sound Status", choices=enum_status, validators=[Optional()], default='')
    graphic = SelectField("Graphics Status", choices=enum_status, validators=[Optional()], default='')
    cocktail = SelectField("Cocktail Status", choices=enum_status, validators=[Optional()], default='')
    protection = SelectField("Protection Status", choices=enum_status, validators=[Optional()], default='')
    savestate = SelectField("SaveState Status", choices=enum_savestate, validators=[Optional()], default='')

    buttons = SelectField("Buttons", choices=[("","")] + [(str(c),str(c)) for c in range(1,18)], validators=[Optional()], default='')
    players = SelectField("Players", choices=[("","")] + [(str(c),str(c)) for c in range(0,8)], validators=[Optional()], default='')

    control_type = SelectField("Control Type", choices=enum_control_type, validators=[Optional()], default='')


@app.route("/search")
@app.route("/search/<int:page>")
def search(page=1):
    """Search view, we need to search by a shitton of values
    Initial thoughts for required values, based on models

    year - select box
    name - text search
    description - text search
    manufacturer - text search (or select?)
    isbios - checkbox
    isdevice - checkbox
    ismechanical - checkbox
    cloneof - "show clones" checkbox

    status - selectbox
    emulation - selectbox
    color - selectbox
    sound - selectbox
    graphic - selectbox
    cocktail - selectbox
    protection - selectbox
    savestate - selectbox

    buttons - selectbox range (1, 17)
    players - selectbox range (0, 7) #who cares, it works
    control.type - selectbox
    """
    form = SearchForm(request.args, csrf_enabled=False)
    results = None

    form.validate()

    print(form.data)

    query = models.Game.query
    if form.year.data != '':
        query = query.filter(models.Game.year == form.year.data)
    if form.name.data != '':
        query = query.filter(models.Game.name.ilike("%%%s%%" % form.name.data))
    if form.description.data != '':
        query = query.filter(models.Game.description.ilike("%%%s%%" % form.description.data))
    if form.manufacturer.data != '':
        query = query.filter(models.Game.manufacturer.ilike("%%%s%%" % form.manufacturer.data))
    if not form.cloneof.data == 'Yes':
        query = query.filter(models.Game.cloneof == None)
    if form.type.data:
        if form.type.data == 'Bios':
            query = query.filter(models.Game.isbios == 'yes')
        elif form.type.data == 'Device':
            query = query.filter(models.Game.isdevice == 'yes')
        elif form.type.data == 'Mechanical':
            query = query.filter(models.Game.ismechanical == 'yes')
    if form.status.data != '':
        query = query.filter(models.Game.status == form.status.data)

    if form.emulation.data != '':
        query = query.filter(models.Game.emulation == form.emulation.data)
    if form.color.data != '':
        query = query.filter(models.Game.color == form.color.data)
    if form.sound.data != '':
        query = query.filter(models.Game.sound == form.sound.data)
    if form.graphic.data != '':
        query = query.filter(models.Game.graphic == form.graphic.data)
    if form.cocktail.data != '':
        query = query.filter(models.Game.cocktail == form.cocktail.data)
    if form.protection.data != '':
        query = query.filter(models.Game.protection == form.protection.data)
    if form.savestate.data != '':
        query = query.filter(models.Game.savestate == form.savestate.data)
    if form.buttons.data != '':
        query = query.filter(models.Game.buttons == form.buttons.data)
    if form.players.data != '':
        query = query.filter(models.Game.players == form.players.data)

    #nasty subselects...
    if form.control_type.data != '':
        query = query.filter(models.Game.control.any(models.Control.type==form.control_type.data))
    if form.rom_status.data != '':
        query = query.filter(models.Game.rom.any(models.Rom.status==form.rom_status.data))
        print(query)

    results = query.paginate(page=page, per_page=25)
    return render_template("search.html", form=form, results=results)