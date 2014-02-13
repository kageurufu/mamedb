mamedb
======

A web based mame game search engine

This project is written in Python 3.3, but works under Python 2.7 and up (maybe lower, I havent tested)

We take full advantage of the wonderful work done by zzzeek on the SQLAlchemy project, as well as mitsuhiko's Flask
and of course, the amazing Python project. By default, the project uses PostgreSQL with the psycopg2 module, but you
can easily swap that out with MySQL/MariaDB/SQLite (although that last one gets kinda slow)

Setup
=====

To create your database, first get a copy of MAME (sdlmame on Arch, http://mamedev.org)

    pip install -r requirements.txt
    /usr/bin/sdlmame --listxml > list.xml
    python manage.py import --reset list.xml
    rm list.xml
    python manage.py runserver

There, you have a full local copy of the MameDB Indexer running, check it out at http://localhost:5000/

Its up to you to figure out where and how to host it

Images
======

Due to giant filesize, and how many there are, I do not provide the Title images used on the site, I got mine from
http://www.mameworld.info

You can use your own collection, or whatever you want. Just put them in static/images/titles/