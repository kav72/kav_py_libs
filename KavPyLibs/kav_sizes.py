"""Модуль работы с единицами измерения из KavPyLibs"""

__version__ = '1.0.0'

from enum import Enum
import logging


class FileDimensionSystems(Enum):
    """Допустимые системы именований размеров файлов"""
    CI = 0
    IEC = 1
    JEDEC = 2

    @classmethod
    def get_default(cls):
        """Получение значения по-умолчанию"""
        return cls.IEC


class FileDimensionCI(Enum):
    """Измерение фалов в системе СИ"""
    # Значения = степень, в которую будет возводиться 1000
    B = 0  # byte
    kB = 1  # kilobyte
    MB = 2  # megabyte
    GB = 3  # gigabyte
    TB = 4  # terabyte
    PB = 5  # petabyte
    EB = 6  # exabyte
    ZB = 7  # zettabyte
    YB = 8  # yottabyte

    @staticmethod
    def get_base() -> int:
        """Получение основания"""
        return 1000

    @classmethod
    def get_default(cls):
        """Получение значения по-умолчанию"""
        return cls.MB


class FileDimensionIEC(Enum):
    """Измерение фалов в системе IEC"""
    # Значения = степень, в которую будет возводиться 1024
    B = 0  # byte
    KiB = 1  # kibibyte
    MiB = 2  # mebibyte
    GiB = 3  # gibibyte
    TiB = 4  # tebibyte
    PiB = 5  # pebibyte
    EiB = 6  # exbibyte
    ZiB = 7  # zebibyte
    YiB = 8  # yobibyte

    @staticmethod
    def get_base() -> int:
        """Получение основания"""
        return 1024

    @classmethod
    def get_default(cls):
        """Получение значения по-умолчанию"""
        return cls.MiB


class FileDimensionJEDEC(Enum):
    """Измерение фалов в системе JEDEC"""
    # Значения = степень, в которую будет возводиться 1024
    B = 0  # byte
    KB = 1  # kilobyte
    MB = 2  # megabyte
    GB = 3  # gigabyte

    @staticmethod
    def get_base() -> int:
        """Получение основания"""
        return 1024

    @classmethod
    def get_default(cls):
        """Получение значения по-умолчанию"""
        return cls.MB


class Sizes:
    """Базовый класс размеров"""
    # Значение
    value = 1.0

    def __init__(self, value: float = 1.0):
        self.value = value


class FileSizes(Sizes):
    """Класс размеров файлов"""

    def __init__(self, value: float, file_dimension, logger: logging.RootLogger = None):
        """
        Конструктор
        :param value: Значение размера файла
        :param file_dimension: Измерение файла (type=FileDimensionCI|FileDimensionIEC|FileDimensionJEDEC)
        :param logger: logger из kav_logging
        """
        super(FileSizes, self).__init__(value=value)
        self.value = value
        self.file_dimension = file_dimension
        # Получаем степень возведения основания по Enum
        self._exponent = file_dimension.value
        self._logger = logger

    def get_bytes(self):
        """Преобразование размера файла в количество байт"""
        return self.value * (self.file_dimension.get_base() ** self._exponent)

    @staticmethod
    def get_from_bytes(size: int, file_dimension_system: FileDimensionSystems):
        """Получение размера файла из количества байт
            @param size: Размер файла в байтах
            @param file_dimension_system: Система именования размеров файлов

            @rtype: FileSizes

        """
        file_dimension_class = FileSizes.get_file_dimension(file_dimension_system)

        # Получаем основание
        base = file_dimension_class.get_base()

        # Получаем максимальное значение измерения в выбранной системе
        file_dimension_length = len(file_dimension_class.__members__)

        exponent = 0
        while size > base and exponent < file_dimension_length-1:
            exponent += 1  # increment the index of the suffix
            size = size / float(base)  # apply the division

        # Получение измерения по степени i (KiB)
        file_dimension = FileSizes.get_file_dimension(file_dimension_system)(exponent)
        # Получение измерения по его имени
        # FileSizes.get_file_dimension(file_dimension_system)['KiB']

        file_size = FileSizes(size, file_dimension)

        return file_size

    @staticmethod
    def get_from_str(stroke: str, file_dimension_system: FileDimensionSystems, logger: logging.RootLogger = None):
        """Получение размера файла из количества байт
            @param stroke: Строка с размером файла
            @param file_dimension_system: Система именования размеров файлов
            @param logger: logger из kav_logging

            @rtype: FileSizes

        """
        i = len(stroke) - 1
        while i >= 0 and stroke[i].isalpha():
            i -= 1

        # Сохраняем класс системы именования размеров файлов
        file_dimension_class = FileSizes.get_file_dimension(file_dimension_system)

        if not(stroke[i + 1:] in file_dimension_class.__members__):
            message = 'В системе именования размеров файлов ' + file_dimension_system.name + \
                      ' не обнаружено измерение '+stroke[i + 1:]
            if logger is not None:
                logger.error(message)
            else:
                print(message)
            return None

        # Получение измерения по его имени
        file_dimension = file_dimension_class[stroke[i + 1:]]

        # Получение значения
        value = float(stroke[:i+1].rstrip())

        file_size = FileSizes(value, file_dimension)

        return file_size

    @staticmethod
    def get_file_dimension(file_dimension_system: FileDimensionSystems):
        """Получаем класс системы именования размеров файлов"""
        if file_dimension_system.value == 0:
            return FileDimensionCI
        elif file_dimension_system.value == 1:
            return FileDimensionIEC
        else:
            return FileDimensionJEDEC

    def __str__(self, precision=2) -> str:
        """Вывод размера файлов в строку
            @param precision: Точность

            @rtype: str
        """
        return "%.*f%s" % (precision, self.value, self.file_dimension.name)
