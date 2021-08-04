"""Модуль работы с путями из KavPyLibs"""
__version__ = '1.1.0'

import os
import fnmatch
import logging
import appdirs


class KavPath:
    """Класс работы с путями"""

    @staticmethod
    def is_network_directory(directory_path: str = "") -> bool:
        """Определение, является ли путь сетевой папкой

        :param directory_path: Путь к каталогу
        :return: bool
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
    def list_files(directory: str, patterns: list, logger: logging.Logger, case_sensitive: bool = False) -> list:
        """Получение списка имен файлов в каталоге с требуемым расширением. Выводятся только имена файлов
         с расширениями без путей к файлам.

        :param directory: Путь к каталогу
        :param patterns: Шаблоны
        :param logger: logger из kav_logging
        :param case_sensitive: Регистрозависимость
        :return: Список имен файлов
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

    @staticmethod
    def get_default_config_dir(app_name):
        """
        Получение дефолтной директории настроек приложения
        Для Windows - в Appdata\Roaming\<app_name>
        Для Linux - в ~/.config/<app_name>

        :param app_name:
        :return: Путь к каталогу настроек
        """
        # Преобразуем имя приложения согласно стандарта ОС
        app_name = KavPath.get_app_name_for_os(app_name)
        # Получаем расположение директории настроек и лог-файла для разных ОС
        settings_dir = appdirs.user_data_dir(appname=app_name, roaming=True, appauthor="") if os.name == 'nt' \
            else appdirs.user_config_dir(appname=app_name, appauthor="")
        return settings_dir

    @staticmethod
    def get_app_name_for_os(app_name):
        """
        Преобразование имени приложения согласно стандартам ОС

        :param app_name: Имя приложения
        :return: Имя приложения по стандартам ОС
        """
        # Для linux имя программы преобразуем в lowercase
        if os.name != 'nt':
            app_name = app_name.lower()
        return app_name
