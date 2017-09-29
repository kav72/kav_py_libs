"""Модуль проверки KavPyLibs"""

__version__ = '1.0.0'

from KavPyLibs.kav_logging import KavLog
from tests import Tests

# Основной ход выполнения программы
print('KavPyLibs ver.'+__version__)

# Получение логгера (с выводом на экран и в файл)
logger = KavLog.get_logger(filename='test.log', log_level=KavLog.nameToLevel["DEBUG"])

# Методы проверки
logger.debug('test')

Tests.test_file_size(logger)



