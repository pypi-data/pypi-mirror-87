import datetime
from typing import List

import click
from flask.cli import with_appcontext

from raspcuterie import db, utils
from raspcuterie.cli import cli


def date_generator(start, stop, **interval):
    while start < stop:
        yield start
        start += datetime.timedelta(**interval)


@cli.group()
def fake():
    """Fake values for your sensors"""


@fake.command(short_help="Fake temperature series")
@with_appcontext
def temperature():
    insert_single_value_data(db.insert_temperature, 5, 25, 60)


@fake.command(short_help="Fake humidity series")
@with_appcontext
def humidity():
    insert_single_value_data(db.insert_humidity, 60, 95)


@fake.command()
@with_appcontext
def weight():
    insert_single_value_data(db.insert_weight, 300, 150)


def insert_single_value_data(db_function, lower, upper, minutes_extra=0):
    today = datetime.datetime.now()
    yesterday = today - datetime.timedelta(hours=24)
    x: List[datetime.datetime] = list(date_generator(yesterday, today, minutes=1))

    with click.progressbar(x) as bar:
        for date in bar:

            z = date + datetime.timedelta(minutes=minutes_extra)

            minute = z.minute + (z.hour % 6 * 60) + minutes_extra

            db_function(utils.time_based_sinus(minute, lower, upper, 1), date)
