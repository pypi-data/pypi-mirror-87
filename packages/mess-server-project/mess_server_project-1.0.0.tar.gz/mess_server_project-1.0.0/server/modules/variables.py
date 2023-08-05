"""Константы для мессенджера"""
import logging


DEFAULT_PORT = 7777
DEFAULT_IP = '127.0.0.1'
MAX_CON = 5
MAX_PACKAGE_LEN = 1024
ENCODING = 'utf-8'
LOGGING_LEVEL = logging.DEBUG
SERVER_DATABASE = 'sqlite:///server_base.db3'
SERVER_CONFIG = 'server.ini'

ACTION = 'action'
TIME = 'time'
USER = 'user'
ACCOUNT = 'account_name'
SENDER = 'from'
DESTINATION = 'to'
DATA = 'bin'
PUBLIC_KEY = 'pubkey'

PRESENCE = 'presence'
RESPONSE = 'response'
ERROR = 'error'
MESSAGE = 'message'
MESSAGE_TEXT = 'message_text'
EXIT = 'Exit'
GET_CONTACTS = 'get_contacts'
LIST_INFO = 'data_list'
REMOVE_CONTACT = 'remove'
ADD_CONTACT = 'add'
USERS_REQUEST = 'get_users'
PUBLIC_KEY_REQUEST = 'pubkey_need'

RESPONSE_200 = {RESPONSE: 200}
RESPONSE_202 = {RESPONSE: 202,
                LIST_INFO: None
                }
RESPONSE_400 = {
    RESPONSE: 400,
    ERROR: None
}
RESPONSE_205 = {
    RESPONSE: 205
}

RESPONSE_511 = {
    RESPONSE: 511,
    DATA: None
}