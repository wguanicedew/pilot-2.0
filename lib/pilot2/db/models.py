# Copyright European Organization for Nuclear Research (CERN)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# You may not use this file except in compliance with the License.
# You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
#
# Authors:
# - Wen Guan, <wen.guan@cern.ch>, 2016

"""
Peewee models for pilot data
"""

import datetime
import inspect
import os
import sys

from peewee import *

from constants import *

work_dir = '.'
if "PILLOT_WORKING_DIR" in os.environ:
    work_dir = os.environ["PILLOT_WORKING_DIR"]
database = SqliteDatabase(os.path.join(work_dir, "pilot.db"))


class ModelBase(Model):
    """Base class for Pilot Models"""
    created_at = DateTimeField(default=datetime.datetime.now)
    updated_at  = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = database


class Job(ModelBase):
    """Job and job metrics"""
    task_id = IntegerField()
    job_id = IntegerField()
    state = JobState()
    execute_command = TextField()
    origin_payload = TextField()  # original payload from panda
    metrics = TextField()

    class Meta:
        primary_key = CompositeKey('task_id', 'job_id')

class File(ModelBase):
    """Files about input, output, logs"""
    task_id = IntegerField()
    job_id = IntegerField()
    type = FileType()  # input, output, logs
    state = FileState
    class Meta:
        constraints = [SQL('FOREIGN KEY(task_id, job_id) '
                           'REFERENCES job(task_id, job_id)')]

class PriorityErrors(ModelBase):
    """Priority errors"""
    task_id = IntegerField()
    job_id = IntegerField()
    priority = IntegerField()
    error_code  = IntegerField(default=1)
    error_diag = TextField()

    class Meta:
        constraints = [SQL('FOREIGN KEY(task_id, job_id) '
                           'REFERENCES job(task_id, job_id)')]


classes = []
clsmembers = inspect.getmembers(sys.modules[__name__], inspect.isclass)
for name, obj in clsmembers:
    if issubclass(obj, ModelBase) and name != 'ModelBase':
        # inspect.getmembers(obj, predicate=inspect.ismethod)
        classes.append(obj)

database.connect()
database.create_tables(classes, safe=True)
database.close()

