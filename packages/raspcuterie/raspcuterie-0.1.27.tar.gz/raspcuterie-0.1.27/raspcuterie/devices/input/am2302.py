from raspcuterie.db import get_db, insert_temperature, insert_humidity
from raspcuterie.devices import InputDevice, LogDevice, DatabaseDevice


class AM2302(InputDevice, LogDevice, DatabaseDevice):
    type = "AM2302"

    DEGREE_CELSIUS = "celsius"
    DEGREE_FAHRENHEIT = "fahrenheit"

    table_sql = """
        create table if not exists {0}
        (
            id    integer primary key,
            time  text not null,
            value integer not null
        );"""

    def __init__(self, name, degree=DEGREE_CELSIUS, gpio=4):
        super(AM2302, self).__init__(name)
        self.pin = gpio
        self.degree = degree

    def read(self):
        humidity, temperature = self.raw()
        return round(humidity, 2), round(temperature, 2)

    def create_table(self, connection):
        connection.execute(AM2302.table_sql.format("humidity"))
        connection.execute(AM2302.table_sql.format("temperature"))

    def raw(self):

        import Adafruit_DHT  # noqa

        sensor = Adafruit_DHT.DHT22

        humidity, temperature = Adafruit_DHT.read_retry(sensor, self.pin, delay_seconds=0.2)

        if temperature and self.degree != "celsius":
            temperature = temperature * 9 / 5 + 32

        return humidity, temperature

    def get_context(self):

        humidity, temperature = self.read()

        return dict(humidity=humidity, temperature=temperature)

    def read_from_database(self):

        time = None

        temperature = (
            get_db()
            .execute("SELECT value, time FROM temperature ORDER BY time DESC LIMIT 1")
            .fetchone()
        )

        if temperature:
            time = temperature[1]
            temperature = temperature[0]

        humidity = (
            get_db()
            .execute("SELECT value, time FROM humidity ORDER BY time DESC LIMIT 1")
            .fetchone()
        )

        if humidity:
            time = humidity[1]
            humidity = humidity[0]

        return humidity, temperature, time

    def temperature_data(self, period="-24 hours", aggregate=5 * 60):

        cursor = get_db().execute(
            """SELECT datetime(strftime('%s', t.time) - (strftime('%s', t.time) % :aggregate), 'unixepoch') time,
       round(avg(value), 2)                                                                value
FROM temperature t
WHERE t.value is not null
  and time >= datetime('now', :period)
GROUP BY strftime('%s', t.time) / :aggregate
ORDER BY time DESC;""",
            dict(period=period, aggregate=aggregate),
        )

        temperature_data = cursor.fetchall()
        cursor.close()
        return temperature_data

    def humidity_data(self, period="-24 hours", aggregate=5 * 60):

        cursor = get_db().execute(
            """SELECT datetime(strftime('%s', t.time) - (strftime('%s', t.time) % :aggregate), 'unixepoch') time,
       round(avg(value), 2)                                                                value
FROM humidity t
WHERE t.value is not null
  and time >= datetime('now', :period)
GROUP BY strftime('%s', t.time) / :aggregate
ORDER BY time DESC;""",
            dict(period=period, aggregate=aggregate),
        )

        humidity_data = cursor.fetchall()

        cursor.close()

        return humidity_data

    def log(self):
        humidity, temperature = self.read()

        insert_humidity(humidity)
        insert_temperature(temperature)
