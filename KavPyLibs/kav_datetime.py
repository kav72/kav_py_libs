"""Модуль работы с датами из KavPyLibs"""
__version__ = '1.0.0'

import socket
import struct
import datetime


class KavDateTime:
    """
    Класс работы с датами
    """

    @staticmethod
    def get_time_from_ntp(address='0.de.pool.ntp.org'):
        """
        Получение даты и времени с NTP-сервера

        :param address: Адрес NTP-сервера
        :return: Кортеж из:
         0 - timestamp - количество секунд с Epoch (1970)
         1 - uct_datetime
         2 - local_datetime
        """
        ref_time_1970 = 2208988800  # Reference time
        client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        data = b'\x1b' + 47 * b'\0'
        client.sendto(data, (address, 123))
        data, address = client.recvfrom(1024)
        t = None
        if data:
            t = struct.unpack('!12I', data)[10]
            t -= ref_time_1970
        return t, datetime.datetime.utcfromtimestamp(t), datetime.datetime.fromtimestamp(t)
