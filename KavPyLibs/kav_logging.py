"""Модуль протоколирования из KavPyLibs"""
__version__ = '1.2.0'

import logging
import os

from logging.handlers import RotatingFileHandler

from KavPyLibs.kav_sizes import FileDimensionSystems
from KavPyLibs.kav_sizes import FileSizes
from KavPyLibs.kav_path import KavPath


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
    def get_logger(filename: str = 'log.txt', log_level=DEBUG, file_size: str = '10MiB', backup_count: int = 2):
        """Инициализация логгера с применением Formatter. Настройка вывода в файл и на экран

        :param filename: Путь к log-файлу
        :param log_level: Уровень детализации протокола. CRITICAL/ERROR/WARNING/INFO/DEBUG/NOTSET
        :param file_size: Размер log-файла в системе IEC
        :param backup_count: Количество файлов предыдущих протоколов
        :return: logging.Logger
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

    @staticmethod
    def get_log_filename(app_name, force_filename) -> str:
        """Определение полного имени файла протоколирования для Windows и Linux.
        Для Windows - в Appdata\Roaming\<app_name>
        Для Linux - если есть каталог в ~/.config/<app_name>, то в нем. Если нет, то в /var/log/<app_name>

        :param app_name: Имя приложения
        :param force_filename: Принудительное полное имя файла настроек

        :return: Полное имя файла настроек
        """
        # Отрабатываем принудительное имя файла настроек
        if force_filename != '':
            return force_filename

        # Преобразуем имя приложения согласно стандартам ОС
        app_name = KavPath.get_app_name_for_os(app_name)

        # Получаем расположение директории настроек и лог-файла для разных ОС
        default_settings_dir = KavPath.get_default_config_dir(app_name)

        # Директорию для протоколов по-умолчанию устанавливаем в директорию настроек
        log_dir = default_settings_dir

        # Для Linux если директория настроек не найдена, то переопределяем на /var/log/app_name
        if os.name != 'nt' and not os.path.exists(default_settings_dir):
            log_dir = f'/var/log/{app_name}'
            print(f'Директория протоколов определена на {default_settings_dir}')

        # Полное имя файла протоколов
        log_filename = os.path.join(log_dir, f'{app_name}.log')

        return log_filename
