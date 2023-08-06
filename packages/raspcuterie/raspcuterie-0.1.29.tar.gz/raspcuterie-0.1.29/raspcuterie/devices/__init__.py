import importlib
import pkgutil
from abc import abstractmethod, ABC
from typing import Dict, Type

import pkg_resources


class DatabaseDevice:
    def create_table(self, connection):
        raise NotImplementedError


class LogDevice:
    def log(self):
        raise NotImplementedError


class EntryPointDiscoverable:
    entry_point: str

    @classmethod
    def discover(cls):
        import raspcuterie.devices.input
        import raspcuterie.devices.output

        for finder, name, ispkg in pkgutil.iter_modules(
            raspcuterie.devices.input.__path__, raspcuterie.devices.input.__name__ + "."
        ):
            importlib.import_module(name)

        for entry_point in pkg_resources.iter_entry_points(cls.entry_point):
            entry_point.load()


class InputDevice(ABC, EntryPointDiscoverable):
    entry_point = "raspcuterie.devices.input"
    type: str
    registry: Dict[str, "InputDevice"] = {}
    types: Dict[str, Type["InputDevice"]] = {}

    def __init__(self, name):
        InputDevice.registry[name] = self
        self.name = name

    def __init_subclass__(cls, **kwargs):
        super(InputDevice, cls).__init_subclass__(**kwargs)

        if hasattr(cls, "type") and cls.type:
            name = cls.type
        else:
            name = cls.__name__

        InputDevice.types[name] = cls

    @abstractmethod
    def read(self):
        raise NotImplementedError

    def get_context(self):
        return {}

    def log(self):
        return


class OutputDevice(ABC, EntryPointDiscoverable):
    entry_point = "raspcuterie.devices.input"
    type: str
    registry: Dict[str, "OutputDevice"] = {}
    types: Dict[str, Type["OutputDevice"]] = {}

    def __init__(self, name):
        OutputDevice.registry[name] = self
        self.name = name

    def __init_subclass__(cls, **kwargs):
        super(OutputDevice, cls).__init_subclass__(**kwargs)
        OutputDevice.types[cls.type] = cls

    @abstractmethod
    def value(self):
        raise NotImplementedError

    def get_context(self):
        return {self.name: self.value()}

    def log(self):
        return
