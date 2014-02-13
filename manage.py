from mame import app
from mame import commands

from flask.ext.script import Manager

manager = Manager(app)
manager.add_command("import", commands.Import)

if __name__ == '__main__':
    manager.run()