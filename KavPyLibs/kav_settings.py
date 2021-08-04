"""Модуль работы с настройками из KavPyLibs"""
__version__ = '1.0.0'

import os
import yaml

from KavPyLibs.kav_path import KavPath


class KavSettings:
    """
    Класс настроек
    """

    @staticmethod
    def load_yaml(filename):
        """
        Загрузка настроек из файла yaml

        :param filename: Имя файла настроек
        :return: Загруженные настройки
        """
        if not os.path.exists(filename):
            exit(-1)

        with open(filename, encoding='utf-8') as settings_file:
            settings = yaml.load(settings_file)
            return settings

    @staticmethod
    def get_settings_filename(app_name, force_filename) -> str:
        """Определение полного имени файла настроек для Windows и Linux.
        Для Windows - в Appdata\Roaming\<app_name>
        Для Linux - если есть каталог в ~/.config/<app_name>, то в нем. Если нет, то в /etc/<app_name>
        Если force_filename не заполнено, то в Windows в случае отсутствия создается каталог настроек
        В Linux не создаем каталог директории - отсутствие ~/.config/<app_name> направляет нас в /etc/<app_name>,
        а там прав на создание все равно не хватит

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
        settings_dir = KavPath.get_default_config_dir(app_name)

        # Для Linux если директория настроек не найдена, то переопределяем на /etc/app_name
        if os.name != 'nt' and not os.path.exists(settings_dir):
            settings_dir = f'/etc/{app_name}'
            print(f'Директория настроек переопределена на {settings_dir}')

        # Если директории настроек нет (и при этом она не /etc/app_name) - создаем ее
        if not os.path.exists(settings_dir) and settings_dir != f'/etc/{app_name}':
            os.makedirs(settings_dir)

        # Полное имя файла настроек
        settings_filename = os.path.join(settings_dir, 'config.yaml')

        return settings_filename
