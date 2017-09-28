__version__ = '1.0.0'

import os
import fnmatch
import logging


class KavPath:
    @staticmethod
    def is_network_directory(directory_path=""):
        """Определение, является ли путь сетевой папкой

        @param directory_path: Путь к каталогу

        @rtype: bool

        """
        # Получаем тип операционной системы: для windows - nt. Для linux - posix
        os_name = os.name

        is_netdir = False
        if os_name == 'nt':
            is_netdir = True if directory_path.startswith('\\\\') else False
        elif os_name == 'posix':
            is_netdir = True if directory_path.startswith('smb://') else False

        return is_netdir

    @staticmethod
    def list_files(directory: str, patterns: list, logger: logging.RootLogger, case_sensitive: bool= False) -> list:
        """Получение списка имен файлов в каталоге с требуемым расширением. Выводятся только имена файлов
         с расширениями без путей к файлам.

        @param directory: Путь к каталогу
        @param patterns: Шаблоны
        @param logger: logger из kav_logging
        @param case_sensitive: Регистрозависимость

        @rtype: list

        """
        if not os.path.exists(directory):
            logger.warning('Каталог '+directory+' не найден. Возвращаем пустой список')
            return []

        all_files = os.listdir(directory)

        i = len(all_files)-1
        # Цикл по именам файлов
        while i >= 0:
            # Совпадение с шаблонами
            is_match = False

            # Цикл по каждому шаблону из списка шаблонов
            for pattern in patterns:
                if case_sensitive and fnmatch.fnmatchcase(all_files[i], pattern) or\
                                not case_sensitive and fnmatch.fnmatch(all_files[i], pattern):
                    is_match = True
                    break
            # Если не нашли ни одного совпадения, то исключаем файл из списка
            if not is_match:
                all_files.remove(all_files[i])

            i -= 1
        logger.debug('По шаблону ' + str(patterns) + ' найдено ' + str(len(all_files)) + ' файлов.')
        return all_files
