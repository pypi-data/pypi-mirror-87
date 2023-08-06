""" QLog logger """

import inspect
import os
from datetime import datetime

from QLog.log_entry import LogEntry

__version__ = "0.1.0"

from QLog.log_level import LogLevel
from QLog.logger import Logger


def QLogHighlight(data):
    log(LogLevel.highlight, data)


def QLogDebug(data):
    log(LogLevel.debug, data)


def QLogInfo(data):
    log(LogLevel.info, data)


def QLogWarning(data):
    log(LogLevel.warning, data)


def QLogError(data):
    log(LogLevel.error, data)


loggers: [Logger] = []


def log(level: LogLevel, data):
    caller = inspect.stack()[2]
    entry = LogEntry(
        datetime.now(),
        os.path.splitext(os.path.basename(caller.filename))[0],
        caller.function,
        caller.lineno,
        level,
        data
    )
    for active_logger in loggers:
        active_logger.log(entry)
