"""Тестирование библиотеки"""

__version__ = '1.0.0'

from KavPyLibs.kav_sizes import FileDimensionIEC
from KavPyLibs.kav_sizes import FileDimensionSystems
from KavPyLibs.kav_sizes import FileSizes


class Tests:
    @staticmethod
    def test_file_size(logger):
        """Тестирование преобразований размеров файлов"""

        dimension = FileDimensionIEC.MiB
        file_size = FileSizes(5, dimension)
        print(str(file_size.value) + file_size.file_dimension.name)
        print(str(file_size.get_bytes()))

        file_size = FileSizes.get_from_bytes(5243560, FileDimensionSystems.IEC)
        print(file_size.__str__())

        s = '5.02miB'
        print(FileSizes.get_from_str(s, FileDimensionSystems.IEC, logger).__str__())