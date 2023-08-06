from pathlib import Path

import yaml
from flask import current_app

from raspcuterie import base_path
from raspcuterie.devices import InputDevice
from raspcuterie.devices.control import ControlRule
from raspcuterie.devices.output.relay import OutputDevice


def parse_config(file: Path):

    InputDevice.discover()
    OutputDevice.discover()

    data = file.read_text()

    data_loaded = yaml.safe_load(data)
    data_loaded["raw"] = data
    return data_loaded


def register_input_devices(config):

    input_devices = config["devices"]["input"]

    for device_name, device in input_devices.items():

        device_type = device.get("type", device_name)

        if device_type in InputDevice.types:

            kwargs = device.copy()
            del kwargs["type"]

            device_class = InputDevice.types[device_type]
            device_class(device_name, **kwargs)
        else:
            current_app.logger.error(f"Cloud not initiate {device}")


def register_output_devices(config):

    input_devices = config["devices"]["output"]

    for device_name, device in input_devices.items():

        device_type = device.get("type", device_name)

        device_class = OutputDevice.types[device_type]

        kwargs = device.copy()

        del kwargs["type"]

        device_class(device_name, **kwargs)


def register_config_rules(config):

    control_rules = config["control"]

    for device, rules in control_rules.items():

        device = OutputDevice.registry[device]

        for rule in rules:

            ControlRule(
                device,
                expression=rule["expression"],
                action=rule["action"],
                name=rule["rule"],
            )


def get_config_file(app):
    if app.debug or app.testing:
        file = Path(__file__).parent.parent.parent / "config_dev.yaml"
    else:
        file = base_path / "config.yaml"

    return file


def setup(app):
    config = parse_config(get_config_file(app))

    app.config["config"] = config["raw"]

    register_input_devices(config)
    register_output_devices(config)
    register_config_rules(config)
