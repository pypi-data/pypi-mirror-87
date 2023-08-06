import configparser
import os
from typing import TypeVar, Generic, Type

import appdirs

T = TypeVar("T")


class StorageValue(Generic[T]):
    app_name: str = None
    name: str = None
    default_value: T = None
    type: Type[T] = None

    def __init__(self, base_dir: str = None):
        self._storage_file = os.path.join(base_dir or self.base_dir, f".{self.name}")
        if os.path.exists(self._storage_file):
            self._value = self.load_value()
        else:
            self._value = self.resolve_default_value()
            self.write_value()

    @property
    def base_dir(self):
        return appdirs.user_config_dir(self.app_name)

    @classmethod
    def read_value_from_file(cls, filename: str, type_: Type[T]) -> T:
        with open(filename, "rt") as file:
            content = file.read()
            return type_(content) if type_ else content

    @classmethod
    def write_value_to_file(cls, filename: str, value: T):
        with open(filename, "wt") as file:
            file.write(str(value))

    def load_value(self) -> T:
        return self.read_value_from_file(self._storage_file, self.type)

    def write_value(self):
        if self._value is not None:
            os.makedirs(os.path.dirname(self._storage_file), exist_ok=True)
            self.write_value_to_file(self._storage_file, self._value)
        # ToDo: else delete file?

    def resolve_default_value(self) -> T:
        return self.default_value

    @property
    def value(self) -> T:
        return self._value

    @value.setter
    def value(self, value: T):
        self._value = value
        self.write_value()


class ConfigValue(StorageValue[configparser.ConfigParser]):
    type = configparser.ConfigParser

    @classmethod
    def read_value_from_file(cls, filename: str, type_: Type[configparser.ConfigParser]) -> configparser.ConfigParser:
        config = type_()
        config.read(filename)
        return config

    @classmethod
    def write_value_to_file(cls, filename: str, value: configparser.ConfigParser):
        with open(filename, "wt") as file:
            value.write(file)
