# Copyright European Organization for Nuclear Research (CERN)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# You may not use this file except in compliance with the License.
# You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
#
# Authors:
# - Wen Guan, <wen.guan@cern.ch>, 2016

"""
Exceptions classes
"""

from ..db.models import PriorityErrors
from ..db.atomic import atomic_lock

class PilotException(Exception):
    """
    To correctly use this class, inherit from it and define
    a 'message' property. That message will get printf'd
    with the keyword arguments provided to the constructor.
    """

    def __init__(self, *args, **kwargs):
        super(LockException, self).__init__(args, kwargs)
        self._message = "Pilot Exception."
        self._error_code = None
        self.args = args
        self.kwargs = kwargs
        self._error_string = None

    def __str__(self):
        try:
            self._error_string = self._message % self.kwargs
        except Exception:
            # at least get the core message out if something happened
            self._error_string = self._message
        if len(self.args) > 0:
            # If there is a non-kwarg parameter, assume it's the error
            # message or reason description and tack it on to the end
            # of the exception message
            # Convert all arguments into their string representations...
            args = ["%s" % arg for arg in self.args if arg]
            self._error_string = (self._error_string + "\nDetails: %s" % '\n'.join(args))
        return self._error_string.strip()

    @atomic_lock
    def save(self, task_id, job_id, priority):
        error = PriorityErrors.create(task_id=task_id,
                                      job_id=job_id,
                                      priority=priority,
                                      error_code=self._error_code,
                                      error_diag=self._error_string)

# classse insert new exceptions in alphabetic order

class NoESEvents(PilotException):
    """
    No more events
    """
    def __init__(self, *args, **kwargs):
        super(AccessDenied, self).__init__(args, kwargs)
        self._message = "No more events."
        self._error_code = 1238


class OverSubscribedESEvents(PilotException):
    """
    OverSubscribed events
    """
    def __init__(self, *args, **kwargs):
        super(AccessDenied, self).__init__(args, kwargs)
        self._message = "Over subscribed events."
        self._error_code = 1239
