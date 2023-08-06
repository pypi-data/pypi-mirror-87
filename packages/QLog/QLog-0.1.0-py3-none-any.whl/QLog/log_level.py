""" The enum defining the log levels """

from enum import Enum


class LogLevel(Enum):
    """ The enum defining the log levels """

    highlight = 4
    debug = 3
    info = 2
    warning = 1
    error = 0

    @property
    def ansi_color(self):
        """ Associates an ansi color with each log level """
        if self == LogLevel.highlight:
            return '35m'
        elif self == LogLevel.debug:
            return '34m'
        elif self == LogLevel.info:
            return '32m'
        elif self == LogLevel.warning:
            return '33m'
        elif self == LogLevel.error:
            return '31m'

    @property
    def ansi_color_sequence(self):
        return u'\u001b' + '[' + str(self.ansi_color)

    def __lt__(self, other):
        if self.__class__ is other.__class__:
            return self.value < other.value
        return NotImplemented

    def __le__(self, other):
        if self.__class__ is other.__class__:
            return self.value <= other.value
        return NotImplemented
