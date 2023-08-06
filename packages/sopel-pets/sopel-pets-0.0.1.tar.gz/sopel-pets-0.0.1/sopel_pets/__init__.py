# coding=utf8
"""sopel-pets

A plugin for Sopel that posts pets in the channel
"""
from __future__ import unicode_literals, absolute_import, division, print_function

from random import seed
from sopel import module
from sqlalchemy import Column, Integer, String
from sqlalchemy import create_engine, event, exc
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.pool import Pool
from sqlalchemy.sql.functions import random


# Define a few global variables for database interaction
Base = declarative_base()


@event.listens_for(Pool, "checkout")
def ping_connection(dbapi_connection, connection_record, connection_proxy):
    cursor = dbapi_connection.cursor()
    try:
        cursor.execute("SELECT 1")
    except:
        # optional - dispose the whole pool
        # instead of invalidating one at a time
        # connection_proxy._pool.dispose()

        # raise DisconnectionError - pool will try
        # connecting again up to three times before raising.
        raise exc.DisconnectionError()
    cursor.close()


class PetsDB(Base):
    __tablename__ = 'pets'
    id = Column(Integer, primary_key=True)
    url = Column(String(255))
    type = Column(String(4))


class Pets:
    @staticmethod
    def add(bot, url, pettype):
        session = bot.db.session()
        # Return False if quote already exists
        if Pets.search(bot, url):
            print('Already Exists')
            return False
        new_pet = PetsDB(url=url, type=pettype)
        session.add(new_pet)
        session.commit()
        session.close()
        return True

    @staticmethod
    def delete(bot, url):
        session = bot.db.session()
        # Return False if quote DNE
        if Pets.search(bot, url):
            return False
        session.query(PetsDB).filter(PetsDB.url == url).delete()
        session.commit()
        session.close()
        return True

    @staticmethod
    def search(bot, url):
        session = bot.db.session()
        res = session.query(PetsDB).filter(PetsDB.url == url).one_or_none()
        session.close()
        return res

    @staticmethod
    def random(bot, pettype):
        session = bot.db.session()
        res = session.query(PetsDB).filter(PetsDB.type == pettype).order_by(random()).first()
        session.close()
        return res


def configure(config):
    pass


def setup(bot):
    # Create tables
    engine = create_engine(bot.db.url)
    Base.metadata.create_all(engine)

    # Initialize our RNG
    seed()


def pets(bot, trigger, pettype):
    # Command called with no argument
    if not trigger.group(2):
        m = Pets.random(bot, pettype)
        if not m:
            return bot.say('ERROR: Unable to get random {0}'.format(pettype))
        return bot.say(m.url)

    # Otherwise add/remove cat
    args = trigger.group(2).split()

    # Error out if URL is too long
    if len(args[1]) > 255:
        return bot.say('ERROR: URL Too Long (>255 characters)')

    # Add Cat
    if args[0].casefold() == 'add'.casefold():
        if not Pets.add(bot, args[1], pettype):  # args[1] should be the URL
            return bot.say('ERROR: {0} already exists'.format(pettype))
        return bot.say('{0} added'.format(pettype))

    # Delete Cat
    elif args[0].casefold() == 'delete'.casefold():
        if not Pets.delete(bot, args[1]):  # args[1] should be the URL
            return bot.say('ERROR: URL Does Not Exist')
        return bot.say('{0}  Deleted'.format(pettype))

    # Otherwise, invalid argument specified
    else:
        return bot.say('Error: Invalid Arguments')


@module.commands('meow')
@module.priority('high')
@module.example('meow')
@module.example('meow add URL')
@module.example('meow delete URL')
def meow(bot, trigger):
    """.meow (add url|delete url) - Post random cat to the channel"""
    pets(bot, trigger, 'meow')


@module.commands('woof')
@module.priority('high')
@module.example('woof')
@module.example('woof add URL')
@module.example('woof delete URL')
def woof(bot, trigger):
    """.woof (add url|delete url) - Post random dog to the channel"""
    pets(bot, trigger, 'woof')
