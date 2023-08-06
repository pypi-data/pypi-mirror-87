import logging


DEFAULT_PORT = 7777                 # Порт поумолчанию для сетевого ваимодействия
# IP адрес по умолчанию для подключения клиента
DEFAULT_IP_ADDRESS = '127.0.0.1'
MAX_CONNECTIONS = 5                 # Максимальная очередь подключений
MAX_PACKAGE_LENGTH = 10240          # Максимальная длинна сообщения в байтах
ENCODING = 'utf-8'                  # Кодировка проекта
LOGGING_LEVEL = logging.DEBUG       # Текущий уровень логирования
SERVER_CONFIG = 'server.ini'        # База данных для хранения данных сервера

# Прококол JIM основные ключи:
ACTION = 'action'
TIME = 'time'
USER = 'user'
ACCOUNT_NAME = 'account_name'
SENDER = 'from'
DESTINATION = 'to'
DATA = 'bin'
PUBLIC_KEY = 'pubkey'

# Прочие ключи, используемые в протоколе
PRESENCE = 'presence'
RESPONSE = 'response'
ERROR = 'error'
MESSAGE = 'message'
MESSAGE_TEXT = 'mess_text'
EXIT = 'exit'
GET_CONTACTS = 'get_contacts'
LIST_INFO = 'data_list'
REMOVE_CONTACT = 'remove'
ADD_CONTACT = 'add'
USERS_REQUEST = 'get_users'
PUBLIC_KEY_REQUEST = 'pubkey_need'

# Словари - ответы:
# 200
RESPONSE_200 = {RESPONSE: 200}
# 202
RESPONSE_202 = {RESPONSE: 202,
                LIST_INFO: None
                }
# 400
RESPONSE_400 = {
    RESPONSE: 400,
    ERROR: None
}

# 205
RESPONSE_205 = {
    RESPONSE: 205
}

# 511
RESPONSE_511 = {
    RESPONSE: 511,
    DATA: None
}
"""
Уровень     Значение    Описание
---------------------------------------------
CRITICAL    50          Критические ошибки/сообщения
ERROR       40          Ошибки
WARNING     30          Предупреждения
INFO        20          Информационные сообщения
DEBUG       10          Отладочная информация
NOTSET      0           Уровень не установлен
"""
