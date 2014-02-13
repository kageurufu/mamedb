from . import db

yn_bool = db.Enum("yes", "no", name="yn_bool")
driver_status = db.Enum("good", "imperfect", "preliminary", name="driver_status")
dump_status = db.Enum("baddump", "nodump", "good", name="dump_status")

class Game(db.Model):
    __tablename__ = "game"
    id = db.Column(db.Integer, primary_key=True)

    biosset       = db.relationship("Biosset",       backref="game")
    rom           = db.relationship("Rom",           backref="game")
    disk          = db.relationship("Disk",          backref="game")
    device_ref    = db.relationship("Device_ref",    backref="game")
    sample        = db.relationship("Sample",        backref="game")
    chip          = db.relationship("Chip",          backref="game")
    display       = db.relationship("Display",       backref="game")
    dipswitch     = db.relationship("Dipswitch",     backref="game")
    configuration = db.relationship("Configuration", backref="game")
    adjuster      = db.relationship("Adjuster",      backref="game")
    device        = db.relationship("Device",        backref="game")
    slot          = db.relationship("Slot",          backref="game")
    softwarelist  = db.relationship("Softwarelist",  backref="game")
    control =       db.relationship("Control",       backref="game")

    name = db.Column(db.String)
    sourcefile = db.Column(db.String)
    isbios = db.Column(yn_bool, default="no")
    isdevice = db.Column(yn_bool, default="no")
    ismechanical = db.Column(yn_bool, default="no")
    runnable = db.Column(yn_bool, default="yes")
    cloneof = db.Column(db.String)
    romof = db.Column(db.String)
    sampleof = db.Column(db.String)
    description = db.Column(db.String)
    year = db.Column(db.String)
    manufacturer = db.Column(db.String)
    service = db.Column(yn_bool, default="no")
    tilt = db.Column(yn_bool, default="no")
    players = db.Column(db.String)
    buttons = db.Column(db.String)
    coins = db.Column(db.String)
    ramoption = db.Column(db.String)
    status = db.Column(driver_status)
    emulation = db.Column(driver_status)
    color = db.Column(driver_status)
    sound = db.Column(driver_status)
    graphic = db.Column(driver_status)
    cocktail = db.Column(driver_status)
    protection = db.Column(driver_status)
    savestate = db.Column(db.Enum("supported", "unsupported", name="driver_savestate"))
    palettesize = db.Column(db.String)
    channels = db.Column(db.String)

class Biosset(db.Model):
    __tablename__ = "biosset"
    id = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(db.Integer, db.ForeignKey(Game.id))
    name = db.Column(db.String)
    description = db.Column(db.String)
    default = db.Column(yn_bool, default="no")

class Rom(db.Model):
    __tablename__ = "rom"
    id = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(db.Integer, db.ForeignKey(Game.id))
    name = db.Column(db.String)
    bios = db.Column(db.String)
    size = db.Column(db.String)
    crc = db.Column(db.String)
    sha1 = db.Column(db.String)
    merge = db.Column(db.String)
    region = db.Column(db.String)
    offset = db.Column(db.String)
    status = db.Column(dump_status, default="good")
    optional = db.Column(yn_bool, default="no")

class Disk(db.Model):
    __tablename__ = "disk"
    id = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(db.Integer, db.ForeignKey(Game.id))
    name = db.Column(db.String)
    sha1 = db.Column(db.String)
    merge = db.Column(db.String)
    region = db.Column(db.String)
    index = db.Column(db.String)
    writable = db.Column(yn_bool, default="no")
    status = db.Column(dump_status, default="good")
    optional = db.Column(yn_bool, default="no")

class Device_ref(db.Model):
    __tablename__ = "device_ref"
    id = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(db.Integer, db.ForeignKey(Game.id))
    name = db.Column(db.String)

class Sample(db.Model):
    __tablename__ = "sample"
    id = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(db.Integer, db.ForeignKey(Game.id))
    name = db.Column(db.String)

class Chip(db.Model):
    __tablename__ = "chip"
    id = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(db.Integer, db.ForeignKey(Game.id))
    name = db.Column(db.String)
    tag = db.Column(db.String)
    type = db.Column(db.Enum("cpu", "audio", name="chip_type"))
    clock = db.Column(db.String)

class Display(db.Model):
    __tablename__ = "display"
    id = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(db.Integer, db.ForeignKey(Game.id))
    tag = db.Column(db.String)
    type = db.Column(db.Enum("raster", "vector", "lcd", "unknown", name="display_type"))
    rotate = db.Column(db.Integer)
    flipx = db.Column(yn_bool, default="no")
    width = db.Column(db.String)
    height = db.Column(db.String)
    refresh = db.Column(db.String)
    pixclock = db.Column(db.String)
    htotal = db.Column(db.String)
    hbend = db.Column(db.String)
    hbstart = db.Column(db.String)
    vtotal = db.Column(db.String)
    vbend = db.Column(db.String)
    vbstart = db.Column(db.String)

class Control(db.Model):
    __tablename__ = "control"
    id = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(db.Integer, db.ForeignKey(Game.id))
    type = db.Column(db.String)
    minimum = db.Column(db.String)
    maximum = db.Column(db.String)
    sensitivity = db.Column(db.String)
    keydelta = db.Column(db.String)
    reverse = db.Column(yn_bool, default="no")
    ways = db.Column(db.String)
    ways2 = db.Column(db.String)
    ways3 = db.Column(db.String)

class Dipswitch(db.Model):
    __tablename__ = "dipswitch"
    id = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(db.Integer, db.ForeignKey(Game.id))
    dipvalue = db.relationship("Dipvalue", backref="dipswitch")
    name = db.Column(db.String)
    tag = db.Column(db.String)
    mask = db.Column(db.String)

class Dipvalue(db.Model):
    __tablename__ = "dipvalue"
    id = db.Column(db.Integer, primary_key=True)
    dipswitch_id = db.Column(db.Integer, db.ForeignKey(Dipswitch.id))
    name = db.Column(db.String)
    value = db.Column(db.String)
    default = db.Column(yn_bool, default="no")

class Configuration(db.Model):
    __tablename__ = "configuration"
    id = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(db.Integer, db.ForeignKey(Game.id))
    confsetting = db.relationship("Confsetting", backref="configuration")
    name = db.Column(db.String)
    tag = db.Column(db.String)
    mask = db.Column(db.String)

class Confsetting(db.Model):
    __tablename__ = "confsetting"
    id = db.Column(db.Integer, primary_key=True)
    configuration_id = db.Column(db.Integer, db.ForeignKey(Configuration.id))
    name = db.Column(db.String)
    value = db.Column(db.String)
    default = db.Column(yn_bool, default="no")

class Adjuster(db.Model):
    __tablename__ = "adjuster"
    id = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(db.Integer, db.ForeignKey(Game.id))
    name = db.Column(db.String)
    default = db.Column(db.String)

class Device(db.Model):
    __tablename__ = "device"
    id = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(db.Integer, db.ForeignKey(Game.id))
    name = db.Column(db.String)
    briefname = db.Column(db.String)
    extension = db.relationship("Extension")
    type = db.Column(db.String)
    tag = db.Column(db.String)
    mandatory = db.Column(db.String)
    interface = db.Column(db.String)

class Extension(db.Model):
    __tablename__ = "extension"
    id = db.Column(db.Integer, primary_key=True)
    device_id = db.Column(db.Integer, db.ForeignKey(Device.id))
    name = db.Column(db.String)

class Slot(db.Model):
    __tablename__ = "slot"
    id = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(db.Integer, db.ForeignKey(Game.id))
    slotoption = db.relationship("Slotoption")
    name = db.Column(db.String)

class Slotoption(db.Model):
    __tablename__ = "slotoption"
    id = db.Column(db.Integer, primary_key=True)
    slot_id = db.Column(db.Integer, db.ForeignKey(Slot.id))
    name = db.Column(db.String)
    devname = db.Column(db.String)
    default = db.Column(yn_bool, default="no")

class Softwarelist(db.Model):
    __tablename__ = "softwarelist"
    id = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(db.Integer, db.ForeignKey(Game.id))
    name = db.Column(db.String)
    status = db.Column(db.Enum("original", "compatible", name="softwarelist_status"))
    filter = db.Column(db.String)
    default = db.Column(db.String)