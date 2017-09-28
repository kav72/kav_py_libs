import logging

__version__ = '1.0.0'


class KavLog:
    CRITICAL = logging.CRITICAL
    FATAL = CRITICAL
    ERROR = logging.ERROR
    WARNING = logging.WARNING
    WARN = WARNING
    INFO = logging.INFO
    DEBUG = logging.DEBUG
    NOTSET = logging.NOTSET

    nameToLevel = {
        'CRITICAL': CRITICAL,
        'ERROR': ERROR,
        'WARN': WARNING,
        'WARNING': WARNING,
        'INFO': INFO,
        'DEBUG': DEBUG,
        'NOTSET': NOTSET,
    }

    @staticmethod
    def get_logger(filename='log.txt', log_level=DEBUG):
        logger = logging.getLogger()
        logger.setLevel(log_level)

        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

        # В файл
        fh = logging.FileHandler(filename=filename, encoding='utf-8')

        # Sets rotation parameters of disk log files
        # https://docs.python.org/3.4/library/logging.handlers.html#rotatingfilehandler
        # handler = logging.handlers.RotatingFileHandler(log_file, maxBytes=10485760, backupCount=2)

        fh.setLevel(log_level)
        fh.setFormatter(formatter)
        logger.addHandler(fh)

        # На экран
        ch = logging.StreamHandler()
        ch.setLevel(log_level)
        ch.setFormatter(formatter)
        logger.addHandler(ch)

        return logger
