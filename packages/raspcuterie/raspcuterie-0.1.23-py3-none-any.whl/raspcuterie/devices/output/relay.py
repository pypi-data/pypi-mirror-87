import datetime
from builtins import super

from flask import current_app

from raspcuterie.db import get_db
from raspcuterie.devices import OutputDevice, DatabaseDevice, LogDevice
from raspcuterie.gpio import GPIO


class RelaySwitch(OutputDevice, DatabaseDevice, LogDevice):
    type = "relay"

    table_sql = """
    create table if not exists {0}
    (
        id    integer primary key,
        time  text not null,
        value integer not null
    );"""

    def __init__(self, name, gpio, timeout=10):
        super(RelaySwitch, self).__init__(name)

        self.pin_number = gpio
        self.timeout_minutes = timeout
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin_number, GPIO.OUT)

    def create_table(self, connection):
        connection.execute(RelaySwitch.table_sql.format(self.table_name))

    def validate_timeout(self):

        with get_db() as db:

            cursor = db.execute(
                """SELECT time FROM {} ORDER BY time DESC LIMIT 1""".format(
                    self.table_name
                )
            )

            result = cursor.fetchone()

            if result and result[0]:
                before = datetime.datetime.now() - datetime.timedelta(
                    minutes=self.timeout_minutes
                )
                last_seen = datetime.datetime.strptime(
                    result[0], "%Y-%m-%d %H:%M:%S.%f"
                )
                current_app.logger.debug(f"{self.name} is last seen on {last_seen}")
                return last_seen < before

        return True

    def _set_output(self, value):
        GPIO.output(self.pin_number, value)

    def _set_value(self, value):
        if self.validate_timeout():
            self._set_output(value)
            self.update_table(self.value())
            return True
        else:
            current_app.logger.debug("Timeout for relay")
            return False

    def on(self):
        self._set_value(GPIO.HIGH)

    def off(self):
        return self._set_value(GPIO.LOW)

    def value(self):
        return GPIO.input(self.pin_number)

    def chart(self, period='-24 hours'):
        cursor = get_db().execute(
            """SELECT time, value
FROM {0} t
WHERE t.value is not null
  and time >= datetime('now', :period)
ORDER BY time DESC;""".format(
                self.table_name
            ), dict(period=period)
        )

        r = cursor.fetchall()
        x = []
        previous_time = None
        for time, value in r:
            if not previous_time:
                previous_time = time
            else:
                x.append((previous_time, value))
                previous_time = time

        return x

    def update_table(self, value, time=None):

        if not time:
            time = datetime.datetime.now()

        db = get_db()

        with db:
            db.execute(
                "INSERT INTO {0}(time,value) VALUES (?,?)".format(self.table_name),
                (time, value),
            )

    @property
    def table_name(self):
        return "relay_" + self.name


class DBRelay(RelaySwitch, DatabaseDevice, LogDevice):
    type = "dbrelay"

    def __init__(self, name, timeout=10, **kwargs):

        super(RelaySwitch, self).__init__(name)
        self.timeout_minutes = timeout

    @property
    def table_name(self):
        return "dbrelay_" + self.name

    def _set_output(self, value):
        self.update_table(value == GPIO.HIGH)

    def value(self):
        cursor = get_db().execute(
            "SELECT value FROM {0} ORDER BY time DESC LIMIT 1".format(self.table_name)
        )

        row = cursor.fetchone()

        if row:
            return bool(row[0])
