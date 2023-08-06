import time
import os
import subprocess
import signal

CHOICE_TEXT = """
1 - запуск сервера
2 - остановка сервера
3 - запуск клиентов 
4 - остановка клиентов
5 - остановить все и выйти
Выберите действие: """

SERVER_FILE_NAME = 'server_class.py'
CLIENT_FILE_NAME = 'chat_gui_ver2.py'

PATH_TO_FILE = os.path.dirname(__file__)
PATH_TO_FILE_CLIENT = PATH_TO_FILE + '/../client_dir/'
PATH_TO_SERVER = os.path.join(PATH_TO_FILE, SERVER_FILE_NAME)
PATH_TO_CLIENT = os.path.join(PATH_TO_FILE_CLIENT, CLIENT_FILE_NAME)
PATH_FOR_MAC_SERVER = os.path.realpath(PATH_TO_SERVER)

SERVER_PROCESE = []
CLIENT_PROCESE = []


def start_server():
    if len(SERVER_PROCESE) == 0:
        try:
            try:
                if os.name == 'posix':
                    server = subprocess.Popen(
                        f'osascript -e \'tell application "Terminal" to do'
                        f' script "python3 {os.path.realpath(PATH_TO_SERVER)}"\'', shell=True)
                    print(server.pid)
                    SERVER_PROCESE.append(server)
                else:
                    server = subprocess.Popen(f'python {PATH_TO_SERVER}', creationflags=subprocess.CREATE_NEW_CONSOLE)
                    SERVER_PROCESE.append(server)
                print('Start_Server')
            except:
                print('Error start_server ')

        except:
            print('ERROR on start server process')
    else:
        print('Server уже создан.')


def stop_server():
    # print(f'Server process count {len(SERVER_PROCESE)}')
    # print('----')
    print(SERVER_PROCESE[0].pid)
    os.killpg(os.getpgid(SERVER_PROCESE[0].pid), signal.SIGKILL)
    # print(f'Server process count after kill {len(SERVER_PROCESE)}')
    # print('----')

    print('Stop_Server')


def start_client():
    client_count = int(input('Сколько клиентов нужно открыть ? '))
    print(client_count)

    for i in range(client_count):
        try:
            if os.name == 'posix':
                client = subprocess.Popen(f'osascript -e \'tell application "Terminal" to do'
                                          f' script "python3 {os.path.realpath(PATH_TO_CLIENT)}"\'', shell=True)
                print(client.pid)
            else:
                client = subprocess.Popen(f'python {PATH_TO_CLIENT}', creationflags=subprocess.CREATE_NEW_CONSOLE)

            CLIENT_PROCESE.append(client)
            print('Start_client')
        except:
            print('Error start client ')
        time.sleep(1)

    print('Start_Client')
    print('----')
    print(f'Client process count {len(CLIENT_PROCESE)}')
    print('----')


def stop_client():
    for i, item in enumerate(CLIENT_PROCESE):
        print(f'PID - {item.pid}')
        pid = item.pid
        os.kill(pid, signal.SIGKILL)
    print('Stop_client')


def stop_all():
    if len(SERVER_PROCESE) > 0:
        stop_server()

    if len(CLIENT_PROCESE) > 0:
        stop_client()

    print('Stop_all')


def start_loop():
    while True:
        print(CHOICE_TEXT)
        CHOISE_VAR = input()
        if CHOISE_VAR == '1':
            start_server()
        elif CHOISE_VAR == '2':
            stop_server()
        elif CHOISE_VAR == '3':
            start_client()
        elif CHOISE_VAR == '4':
            stop_client()
        elif CHOISE_VAR == '5':
            stop_all()
            break


if __name__ == '__main__':
    print(PATH_TO_CLIENT)
    start_loop()