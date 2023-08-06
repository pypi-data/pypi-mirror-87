"""  The log entry to be used for logging """

from datetime import date
from typing import NamedTuple

from QLog.log_level import LogLevel


class LogEntry(NamedTuple):
    """  The log entry to be used for logging """

    date: date
    file: str
    function: str
    line: int
    log_level: LogLevel
    text: str

    @property
    def meta_text(self):
        """  The meta data of a log entry containing date, file, line and function """

        return str(self.date) + ': ' + self.file + ':' + str(self.line) + ' ' + self.function + ': '
