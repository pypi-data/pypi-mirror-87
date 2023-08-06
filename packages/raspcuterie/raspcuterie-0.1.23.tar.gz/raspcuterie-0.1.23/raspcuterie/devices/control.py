from typing import List

from flask import current_app

from raspcuterie.devices import InputDevice
from raspcuterie.devices import OutputDevice


class ControlRule:
    registry: List["ControlRule"] = []

    def __init__(self, device: OutputDevice, expression: str, action: str, name: str = None):
        ControlRule.registry.append(self)
        self.name = name
        self.device: OutputDevice = device
        self.expression: str = expression
        self.action: str = action

    @staticmethod
    def context():
        context = {}

        for device in InputDevice.registry.values():
            context.update(device.get_context())
        return context

    def matches(self):
        return eval(self.expression, self.context())

    def execute(self):
        try:
            action = getattr(self.device, self.action)
            return action()
        except Exception as e:
            current_app.logger.exeception(e)

    def execute_if_matches(self):
        if self.matches():
            current_app.logger.info(f"Matches expression {self.expression}, executing {self.name}.{self.action}")
            return self.execute()
        else:
            current_app.logger.info(f"Does not match expression: {self.expression}")
