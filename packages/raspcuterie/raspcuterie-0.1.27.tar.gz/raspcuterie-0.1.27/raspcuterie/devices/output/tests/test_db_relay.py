from raspcuterie.db import get_db
from raspcuterie.devices.output.relay import DBRelay


def test_on(app):

    with app.app_context():
        x = DBRelay("test")
        x.create_table(get_db())
        x.on()

        assert x.value() is True


def test_off(app):

    with app.app_context():
        x = DBRelay("test")

        x.off()

        assert x.value() is False
