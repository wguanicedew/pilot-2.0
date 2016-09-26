# Copyright European Organization for Nuclear Research (CERN)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# You may not use this file except in compliance with the License.
# You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
#
# Authors:
# - Wen Guan, <wen.guan>, 2016

"""
Constants.

Each constant is in the format:
    CONSTANT_NAME = VALUE, DESCRIPTION
VALUE is what will be stored in the DB.
DESCRIPTION is the meaningful string for client
"""

from peewee import Field


class EnumFiledMeta(type):
    """Generate new EnumField classes."""

    def __init__(cls, classname, bases, dict_):
        cls.db_field = classname.lower()
        cls._values = cls._values.copy()

        for k, v in dict_.items():
            if not k.startswith("__") and not k.startswith("_"):
                cls._values[v] = k
        return type.__init__(cls, classname, bases, dict_)

    def __iter__(cls):
        return iter(cls._values.keys())



class BaseEnumField(Field):
    """Base Enum Field"""
    __metaclass__ = EnumFiledMeta
    db_field = 'baseenumfield'
    _values = {}

    def db_value(self, value):
        try:
            self._values[value]
            return value
        except KeyError:
            raise ValueError("Invalid value for %r: %r" % (self.__class__.__name__, value))

    def python_value(self, value):
        try:
            key = self._values[value]
            return getattr(self, key)
        except KeyError:
            raise ValueError("Invalid value for %r: %r" % (self.__class__.__name__, value))


class JobState(BaseEnumField):
    STARTING1 = 'starting'
    RUNNING = 'running'
    HOLDING = 'holding'
    TOBEKILLED = 'tobekilled'
    TRANSFERING = 'transfering'
    FINISHED = 'finished'
    FAILED = 'failed'


class FileType(BaseEnumField):
    INPUT = 'input'
    OUTPUT = 'output'
    LOG = 'log'


class FileState(BaseEnumField):
    NOTCREATED = 'notcreated'
    CREATED = 'created'
    TRANSFERED = 'transfered'
    GETFAILED = 'getfailed'
    PUTFAILED = 'putfailed'
