"""Модуль протоколирования из KavPyLibs"""
__version__ = '1.1.0'

import logging
from logging.handlers import RotatingFileHandler

from KavPyLibs.kav_sizes import FileDimensionSystems
from KavPyLibs.kav_sizes import FileSizes


class KavLog:
    """Класс протоколирования"""

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
    def get_logger(filename: str = 'log.txt', log_level=DEBUG, file_size: str = '10MiB', backup_count: int = 2)\
            -> logging.RootLogger:
        """Инициализация логгера с применением Formatter. Настройка вывода в файл и на экран

                @param filename: Путь к log-файлу
                @param log_level: Уровень детализации протокола. CRITICAL/ERROR/WARNING/INFO/DEBUG/NOTSET
                @param file_size: Размер log-файла в системе IEC
                @param backup_count: Количество файлов предыдущих протоколов

                @rtype: logging.RootLogger

        """
        # Конвертируем file_size из строковой записи в размер файла
        file_size = FileSizes.get_from_str(file_size, FileDimensionSystems.IEC)
        if file_size is None:
            print('Не удалось распознать максимальный размер log-файла')
            return None
        # Получаем количество байтов
        max_bytes = file_size.get_bytes()

        logger = logging.getLogger()
        logger.setLevel(log_level)

        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

        # В файл
        # fh = logging.FileHandler(filename=filename, encoding='utf-8')
        fh = RotatingFileHandler(filename=filename, encoding='utf-8', maxBytes=max_bytes, backupCount=backup_count)
        # 10485760 = 10Mb

        fh.setLevel(log_level)
        fh.setFormatter(formatter)
        logger.addHandler(fh)

        # На экран
        ch = logging.StreamHandler()
        ch.setLevel(log_level)
        ch.setFormatter(formatter)
        logger.addHandler(ch)

        logger.debug('=====================================================================')
        logger.debug('Инициализирован log-файл максимальным размером %s с количеством предыдущих протоколов %i'
                     % (file_size.__str__(), backup_count))
        return logger
