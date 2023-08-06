import base64
import json

from common.vars import ENCODE_LANG, MAX_LENG, MESSAGE_TEXT, SECRET_KEY, ACTION, MESSAGE
from Crypto.Cipher import AES


# Функция получения сообщения с последующим декодированием
def get_message(client):
    encode_resp = client.recv(MAX_LENG)
    if isinstance(encode_resp, bytes):
        json_resp = encode_resp.decode(ENCODE_LANG)
        resp = json.loads(json_resp)

        if isinstance(resp, dict):
            print('RESP =====')
            print(resp)
            print(type(resp))
            if ACTION in resp and resp[ACTION] == MESSAGE and MESSAGE_TEXT in resp:
                message = resp[MESSAGE_TEXT]
                print(f'MESSAGE TEXT IS COME {message}')
                print('---------')
                message = message.encode('ascii')
                dec_mes = base64.b64decode(message)
                message = decript(dec_mes, SECRET_KEY)
                resp[MESSAGE_TEXT] = message
            return resp
        else:
            print('Error')
    else:
        print('Incorrect Data from get_message')


# Функция передачи сообщения с шифрованием
def send_msg_finish(socket, msg):
    print('Sending message..')
    if not isinstance(msg, dict):
        raise print('ERROR DICT SEND MSG')
    print('msg_for_send')
    print(msg)
    if MESSAGE_TEXT in msg:
        print('MSG_CODE')
        message = msg[MESSAGE_TEXT]
        message = padding_text(message)
        message_cript = cript(message, SECRET_KEY)
        encode_msg = base64.b64encode(message_cript)
        encode_msg = encode_msg.decode('ascii')
        msg[MESSAGE_TEXT] = encode_msg
        print(msg)
        print('-----')
    else:
        pass
    print('JSON_dumps')
    js_msg = json.dumps(msg)
    print('Send msg from send_msg_finish', js_msg)
    encode_msg = js_msg.encode(ENCODE_LANG)
    socket.send(encode_msg)
    print('Send OK')


# Добавление padding для шифрования
def padding_text(text):
    message = text
    message = message.encode('utf-8')
    print(message)
    print('---')
    pad_len = (16 - len(message) % 16) % 16
    return message + b' ' * pad_len


# Функция шифрования сообщения
def cript(msg, key):
    print(len(msg))
    crip = AES.new(key, AES.MODE_CBC)
    ciphertext = crip.iv + crip.encrypt(msg)
    return ciphertext


# Функция дешивроки сообщения
def decript(msg, key):
    crip = AES.new(key, AES.MODE_CBC, iv=msg[:16])
    msg_decrypt = crip.decrypt(msg[16:])
    msg_decrypt = msg_decrypt.decode('utf-8')
    return msg_decrypt
