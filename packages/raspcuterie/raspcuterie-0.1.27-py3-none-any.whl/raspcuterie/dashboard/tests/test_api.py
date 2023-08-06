import datetime

import pytest

from raspcuterie.db import get_db
from raspcuterie.devices import OutputDevice
from raspcuterie.devices.input.am2302 import AM2302
from raspcuterie.devices.output.relay import DBRelay


@pytest.fixture
def relay(app):

    relay_name = "temp"
    device = DBRelay(relay_name)

    assert relay_name in OutputDevice.registry

    with app.app_context():

        device.create_table(get_db())

        device.update_table(False, datetime.datetime.now() - datetime.timedelta(days=100))

        assert device.value() is False

    return device


@pytest.fixture()
def am2302(app):

    am2302 = AM2302("temperature")
    with app.app_context():
        am2302.create_table(get_db())

    return am2302


def test_relay_toggle(client, relay):

    response = client.post("api/relay/temp/toggle")

    data = response.get_json()

    assert data["state"] == relay.value() is True


def test_relay_current(client, relay):

    response = client.get("api/relay/current.json")

    assert response.status_code == 200, response.status_code

    data = response.get_json()

    assert data[relay.name] == relay.value()


def test_am2303_chart(app, monkeypatch, client, am2302):
    temperature = 22
    humidity = 82
    monkeypatch.setattr(AM2302, "read", lambda self: (humidity, temperature))

    with app.app_context():
        am2302.log()

    response = client.get("api/am2302/chart.json")

    assert response.status_code == 200

    data = response.get_json()

    assert data["temperature"][0]["data"][0][1] == temperature
    assert data["humidity"][0]["data"][0][1] == humidity
