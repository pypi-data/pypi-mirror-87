#!/usr/bin/env python3.6
# -*- Coding: UTF-8 -*-
'''
Scheduler Bot.

Copyright 2020 Eduardo S. Pereira

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
'''
from datetime import datetime, timedelta
import sched
import time
import os
import sys
import logging
import inspect


class NotFunctionOperator(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class HoursError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class MinutesError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class Bot:
    '''    Scheduler Bot.
    '''

    def __init__(self, LOGSPATH, CACHEDIR,  verbose=True, deltatime=24):
        self._verbose = verbose
        self._deltatime = deltatime

        if os.path.isdir(LOGSPATH) is False:
            os.makedirs(LOGSPATH)

        if os.path.isdir(CACHEDIR) is False:
            os.makedirs(CACHEDIR)

        self.logger = logging.getLogger()
        _format = "%(asctime)-15s %(message)s"
        loggin_name = "/bot_{0}.log".format(datetime.now().strftime(
            "%Y%m%dT%H%M%S"))
        logging.basicConfig(filename=f'{LOGSPATH}{loggin_name}',
                            level=logging.DEBUG,
                            format=_format
                            )

        urllib3_log = logging.getLogger("urllib3")
        urllib3_log.setLevel(logging.CRITICAL)

        self._print("The Scheduler is Starting.")

        self._scheduler = sched.scheduler(timefunc=time.time,
                                          delayfunc=time.sleep)

        self._next_time = None
        self._operationfunc = None

    def _print(self, msg):
        self.logger.info(msg)
        if self._verbose is True:
            print(msg)

    def _operantions(self):
        if self._operationfunc is None:
            raise NotFunctionOperator("Operation Function not defined.")

        if callable(self._operationfunc) is False:
            msg = "Operation must be a function without parameters."
            raise NotFunctionOperator(msg)

        parms = len(inspect.getargspec(self._operationfunc)[0])

        if parms != 0:
            msg = "Operation must be a function without parameters."
            raise NotFunctionOperator(msg)

        self._operationfunc()

    def _rescheduler(self):
        info = "The Bot is starting!"
        self._print(info)
        self._operantions()
        self._reset_time()
        info = "The bot will be restarted at: {}".format(
            self._next_time)

        self._print(info)

    def _reset_time(self):
        """Set the next start time to process.
        """
        self._next_time = self._next_time + timedelta(minutes=self._deltatime)
        current_time = datetime.now()
        delta_time = self._next_time - current_time
        if delta_time.total_seconds() < 0:
            self._next_time = current_time + timedelta(minutes=self._deltatime)

        self._scheduler.enterabs(time.mktime(self._next_time.timetuple()),
                                 priority=0,
                                 action=self._rescheduler,
                                 argument=())

    def _set_time(self):
        """Set the start time to process.
        """
        current_time = datetime.now()
        set_time = current_time.replace(hour=self.hours, minute=self.minutes)
        delta_time = set_time - current_time
        if delta_time.total_seconds() < 0:
            next_time = current_time + timedelta(hours=24)
            next_time = next_time.replace(hour=self.hours, minute=self.minutes)
        else:
            next_time = set_time

        self._next_time = next_time
        info = "The bot will be started at: {}".format(
            self._next_time)

        self._print(info)
        self._scheduler.enterabs(time.mktime(next_time.timetuple()),
                                 priority=0,
                                 action=self._rescheduler,
                                 argument=())

    def run(self, hours, minutes):
        """Start the scheduler.
        Start the scheduler to run the Transfer in autonomous mode.

        Args:
            hours (int): 
                the hour of firts Transfer start
            minutes (int): 
                the minutes of firts Transfer start
        """
        self.hours = hours
        self.minutes = minutes

        self._set_time()
        try:
            self._scheduler.run()
        except KeyboardInterrupt:
            self._print("Stopping the Bot.")

    @property
    def operations(self):
        return self._operationfunc

    @operations.setter
    def operations(self, func):
        self._operationfunc = func

    @property
    def hours(self):
        return self._hours

    @property
    def minutes(self):
        return self._minutes

    @hours.setter
    def hours(self, h):
        if h > 23 or h < 0:
            raise HoursError("Hours must be in range 0-23: {}".format(h))
        self._hours = h

    @minutes.setter
    def minutes(self, m):
        if m < 0 or m > 60:
            raise MinutesError("Minutes must be in range 0-60: {}".format(m))
        self._minutes = m
