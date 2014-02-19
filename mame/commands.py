from lxml import etree
from . import models, db
from flask.ext.script import Command, Option, prompt_bool

modelmap = {
    'biosset': models.Biosset,
    'rom': models.Rom,
    'disk': models.Disk,
    'device_ref': models.Device_ref,
    'sample': models.Sample,
    'chip': models.Chip,
    'display': models.Display,
    'control': models.Control,
    'dipswitch': models.Dipswitch,
    'dipvalue': models.Dipvalue,
    'configuration': models.Configuration,
    'confsetting': models.Confsetting,
    'adjuster': models.Adjuster,
    'device': models.Device,
    'extension': models.Extension,
    'slot': models.Slot,
    'slotoption': models.Slotoption,
    'softwarelist': models.Softwarelist    
}

class Import(Command):
    option_list = (
        Option("file", help="the file output from mame -listxml"),
        Option("-r", "--reset", action="store_true", help="Recreate the whole database")
    )

    def run(self, file, reset):
        if reset:
            db.drop_all()
            db.create_all()

        print("Beginning import of %s" % file)
        #listfile = open(file, "r")
        #listxml = listfile.read()
        #print("Read file into memory")

        mame = etree.iterparse(file, tag="game")
        i = 0
        g = 0
        for event, elem in mame:
            game = models.Game(**elem.attrib)
            for child in elem:
                if child.tag in ('description', 'year', 'manufacturer', 'ramoption'):
                    setattr(game, child.tag, child.text)
                elif child.tag in ('driver', 'sound'):
                    for k,v in child.attrib.iteritems():
                        setattr(game, k, v)
                elif child.tag == 'input':
                    for k,v in child.attrib.iteritems():
                        setattr(game, k, v)
                    for subchild in child:
                        #These should only be "control" instances
                        game.control.append(modelmap['control'](**subchild.attrib))
                elif child.tag in ('port'): # We ignore these, they are stupid anyway
                    pass
                else:
                    childmodel = modelmap[child.tag](**child.attrib)
                    if child.tag in ('input', 'dipswitch', 'configuration', 'device', 'slot'):
                        for subchild in child:
                            if subchild.tag == 'instance':
                                for k,v in subchild.attrib.items():
                                    setattr(childmodel, k, v)
                            else:
                                subchildmodel = modelmap[subchild.tag](**subchild.attrib)
                                getattr(childmodel, subchild.tag, []).append(subchildmodel)
                            subchild.clear()
                    getattr(game, child.tag, []).append(childmodel)
                child.clear()
            db.session.add(game)
            i += 1
            g += 1
            if i == 100:
                i = 0
                db.session.commit()
                print("%s games imported" % g)
            elem.clear()
            while elem.getprevious() is not None:
                del elem.getparent()[0]
        db.session.commit()
        del mame
        print("Import complete, %s games imported total" % g)

class SetupDB(Command):
    option_list = (
        Option("-y", "--yes", action="store_true", help="Don't verify before recreating the database")
    )

    def run(self, yes):
        if not yes:
            if not prompt_bool("Are you sure, this will erase all information in the database", default=False):
                return 0
        print("Dropping all tables")
        db.drop_all()
        print("Creating the blank database")
        db.create_all()
        print("Database created, you may now import your list.xml")