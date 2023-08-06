import logging

from flask import current_app

from raspcuterie.cli import cli, with_appcontext
from raspcuterie.devices import InputDevice, OutputDevice
from raspcuterie.devices.control import ControlRule


def evaluate_config_rules():
    for rule in ControlRule.registry:
        rule.execute_if_matches()


@cli.command(short_help="Log the input and output devices")
@with_appcontext
def log():
    current_app.logger.setLevel(logging.DEBUG)
    try:
        evaluate_config_rules()
    except Exception as e:
        current_app.logger.error(e)

    for input_device in InputDevice.registry.values():
        try:
            input_device.log()
        except Exception as e:
            current_app.logger.error(e)

    for output_device in OutputDevice.registry.values():
        try:
            output_device.log()
        except Exception as e:
            current_app.logger.error(e)
