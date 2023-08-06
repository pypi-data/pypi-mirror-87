import QLog
from QLog.console_logger import ConsoleLogger
from QLog import QLogHighlight, QLogDebug, QLogInfo, QLogWarning, QLogError


def main():
    QLog.loggers = [ConsoleLogger()]
    QLogHighlight('Test')
    QLogDebug('Test')
    QLogInfo('Test')
    QLogWarning('Test')
    QLogError('Test')


if __name__ == '__main__':
    main()
