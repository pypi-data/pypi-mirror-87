"""  Logger to log into console """

from QLog.log_entry import LogEntry
from QLog.log_level import LogLevel
from QLog.logger import Logger


class ConsoleLogger(Logger):
    """  Logger to log into console """

    def __init__(self, log_level=LogLevel.highlight):
        self.log_level = log_level

    escape = u'\u001b'
    ansi_bold = '1m'
    ansi_reset = '0m'
    ansi_text_color = '37m'

    ansi_bold_sequence = escape + '[' + ansi_bold
    ansi_reset_sequence = escape + '[' + ansi_reset
    ansi_text_sequence = escape + '[' + ansi_text_color

    def do_log(self, log_entry: LogEntry):
        print(
            ConsoleLogger.ansi_bold_sequence +
            ConsoleLogger.ansi_text_sequence +
            log_entry.meta_text +
            ConsoleLogger.ansi_bold_sequence +
            log_entry.log_level.ansi_color_sequence +
            log_entry.text +
            ConsoleLogger.ansi_reset_sequence
        )
