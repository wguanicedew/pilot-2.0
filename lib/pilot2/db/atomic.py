# Copyright European Organization for Nuclear Research (CERN)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# You may not use this file except in compliance with the License.
# You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
#
# Authors:
# - Wen Guan, <wen.guan@cern.ch>, 2016

"""
Atomic lock
"""

import os
import sys
import time

from functools import wraps

work_dir = '.'
if "PILLOT_WORKING_DIR" in os.environ:
    work_dir = os.environ["PILLOT_WORKING_DIR"]
default_lock = os.path.join(work_dir, "pilot2_atomic.lock")


class LockException(Exception):
    """
    To correctly use this class, inherit from it and define
    a 'message' property. That message will get printf'd
    with the keyword arguments provided to the constructor.
    """

    def __init__(self, *args, **kwargs):
        super(LockException, self).__init__(args, kwargs)
        self._message = "Exception to get the lock."
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


class AtomicLock(object):
    def __init__(self, lockFile=None, block=False, timeout=5):
        if lockFile:
            self.__lockFile = lockFile
        else:
            self.__lockFile = default_lock
        self.__lockFD = None
        self.__block = block
        self.__timeout = timeout

    def __enter__(self):
        timeStart = time.time()
        exception = None
        while self.__block or (time.time() < timeStart + self.__timeout):
            try:
                # acquire the lock
                self.__lockFD = os.open(self.__lockFile, os.O_EXCL|os.O_CREAT)
                break
            except OSError, e:
                # already locked
                exception = e
                self.__lockFD = None
                time.sleep(0.01)
        if not self.__lockFD:
            raise LockException(e.args)

    def __exit__(self, exc_type, exc_val, exc_traceback):
        try:
            os.close(self.__lockFD)
            os.unlink(self.__lockFile)
        except Exception, e:
            raise LockException(e.args)

    def acquire(self, block=False, timeout=5):
        self.__block = block
        self.__timeout = timeout
        self.__enter__()

    def release(self):
        self.__exit__()


def atomic_lock(*dargs, **dkw):
    """
    Decorator that gets the lock before run a function.
    Usage example:
    1) Without parameters
        @atomic_lock
        def function(lock=None)
    2) With parameters
        @atomic_lock(lockFile='tmp.lock', block=False, timeout=10)
        def function(lock=None)
    """
    if len(dargs) == 1 and callable(dargs[0]):
        def wrap_simple(function):
            @wraps(function)
            def new_funct(*args, **kwargs):
                if not kwargs.get('lock'):
                    with AtomicLock() as lock:
                        kwargs['lock'] = lock
                        try:
                            return function(*args, **kwargs)
                        except:
                            raise
            new_funct.__doc__ = function.__doc__
            return new_funct
        return wrap_simple(dargs[0])
    else:
        def wrap_comp(function):
            @wraps(function)
            def new_funct(*args, **kwargs):
                if not kwargs.get('lock'):
                    with AtomicLock(*dargs, **dkw) as lock:
                        kwargs['lock'] = lock
                        try:
                            return function(*args, **kwargs)
                        except:
                            raise
            new_funct.__doc__ = function.__doc__
            return new_funct
        return wrap_comp
