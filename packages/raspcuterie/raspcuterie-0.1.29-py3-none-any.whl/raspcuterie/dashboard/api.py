from flask import Blueprint, jsonify, request
from flask_babel import gettext

from raspcuterie.db import get_db
from raspcuterie.devices import InputDevice
from raspcuterie.devices.input.am2302 import AM2302
from raspcuterie.devices.output.relay import OutputDevice, RelaySwitch

bp = Blueprint("api", __name__, url_prefix="/api")


def slope(table):
    x_series = range(1, 6)
    x_average = sum(x_series) / 5

    series = get_db().execute(
        "SELECT value FROM {} ORDER BY time DESC LIMIT 5".format(table)
    )

    y_series = list(reversed([x[0] for x in series.fetchall()]))

    y_average = sum(y_series) / 5

    average_delta = sum(
        [(x - x_average) * (y - y_average) for x, y in zip(x_series, y_series)]
    )

    # we have a series of 5
    x_constant = 10

    return round(average_delta / x_constant, 2)


def min_max_over_period(table: str, period="-24 hours"):
    result = get_db().execute(
        """SELECT min(value), max(value)
FROM {} as t
WHERE t.value is not null
  and t.time >= datetime('now', :period)""".format(
            table
        ),
        dict(period=period),
    )
    min_value, max_value = result.fetchone()

    if not min_value:
        min_value = 0

    if not max_value:
        max_value = 0

    return min_value, max_value


@bp.route("/am2302/current.json")
def am2303_current():
    """
    Returns the current values for the humidity and temperature
    :return:
    """
    from raspcuterie.devices import InputDevice

    humidity, temperature, time = InputDevice.registry[
        "temperature"
    ].read_from_database()

    temperature_slope = slope("temperature")
    humidity_slope = slope("humidity")

    period = request.args.get("period", "-24 hours")

    temperature_min_max = min_max_over_period("temperature", period)
    humidity_min_max = min_max_over_period("humidity", period)

    temperature = dict(
        current=temperature,
        min=round(temperature_min_max[0], 2),
        max=round(temperature_min_max[1], 2),
        slope=temperature_slope,
    )

    humidity = dict(
        current=humidity,
        min=humidity_min_max[0],
        max=humidity_min_max[1],
        slope=humidity_slope,
    )

    return jsonify(dict(temperature=temperature, humidity=humidity, time=time))


@bp.route("/am2302/chart.json")
def am2303_chart():
    am2302: AM2302 = InputDevice.registry["temperature"]

    refrigerator: RelaySwitch = OutputDevice.registry["refrigerator"]
    heater: RelaySwitch = OutputDevice.registry["heater"]

    humidifier: RelaySwitch = OutputDevice.registry["humidifier"]
    dehumidifier: RelaySwitch = OutputDevice.registry["dehumidifier"]

    period = request.args.get("period", "-24 hours")
    aggregate = request.args.get("aggregate", 5 * 60)

    return jsonify(
        dict(
            temperature=[
                dict(
                    name=gettext("Temperature"),
                    data=am2302.temperature_data(period, aggregate),
                ),
                dict(name=gettext("Refrigerator"), data=refrigerator.chart(period)),
                dict(name=gettext("Heater"), data=heater.chart(period)),
            ],
            humidity=[
                dict(
                    data=am2302.humidity_data(period, aggregate),
                    name=gettext("Humidity"),
                ),
                dict(data=humidifier.chart(period), name=gettext("Humidifier")),
                dict(data=dehumidifier.chart(period), name=gettext("Dehumidifier")),
            ],
        )
    )


@bp.route("/relay/current.json")
def relay_current():
    from raspcuterie.devices import OutputDevice

    data = {}

    for key, device in OutputDevice.registry.items():
        if isinstance(device, RelaySwitch):
            data[key] = device.value()

    return jsonify(data)


@bp.route("/relay/<name>/toggle", methods=["POST", "GET"])
def relay_toggle(name):
    device = OutputDevice.registry[name]

    if device.value() == 0:
        device.on()
    else:
        device.off()

    return jsonify(dict(state=device.value()))
