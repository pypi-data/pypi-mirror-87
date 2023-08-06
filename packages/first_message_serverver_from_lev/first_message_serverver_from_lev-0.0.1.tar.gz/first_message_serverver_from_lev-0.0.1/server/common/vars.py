DEF_PORT = 64000
# DEF_IP = '192.168.0.26'
DEF_IP = 'localhost'
MAX_CONNECTIONS = 3
MAX_LENG = 4096
ENCODE_LANG = 'utf-8'
# ACCOUNT_NAME = "Егорка"
PASSWORD_USER = "1235"
DEF_IP_ADDRES_FOR_CLIENT = 'localhost'



# Протокол JIM

ACTION = 'action'
TIME = 'time'
USER = 'user'
ACCOUNT_NAME = 'account_name'
PASSWORD_HASH = 'password_hash'
SENDER = 'from'
DESTINATION = 'to'
USER_ID_TO_CONTACT = 'user_to_list'



# Прочие ключи

PRESENCE = 'presence'
RESPONCE = 'responce'
ERROR = 'error'
MESSAGE = 'message'
MESSAGE_TEXT = 'mess_text'
EXIT = 'exit'
GET_CONTACT = 'get_contacts'
ADD_CONTACT = 'add_contact'
DEL_CONTACT = 'del_contact'
DATA = 'data'
MSG_RESP = 'MSG_RESP'
CONTACT_LOST = 'contact_list'
REGISTER = 'register_user'
LOGIN = 'user_login'
LOGIN_REQUEST = 'login_request'


RESPONCE_200 = {RESPONCE:200}

RESPONCE_400 = {RESPONCE:400}

RESPONCE_ERROR = {
    RESPONCE: 400,
    ERROR: None
}


RESPONCE_202 = {
    RESPONCE: 202,
    DATA: None
}

CUSTOM_RESPONCE = {
    RESPONCE: None,
    MSG_RESP: None

}

RESPONCE_511 = {RESPONCE:511}

SECRET_KEY = b'5555555555555555'

