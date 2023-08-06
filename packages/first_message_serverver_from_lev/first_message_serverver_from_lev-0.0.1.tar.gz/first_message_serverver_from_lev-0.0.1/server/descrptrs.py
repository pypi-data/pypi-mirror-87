import logging
logger = logging.getLogger('server')

# Дескриптор для описания порта:
class Port:
    '''
     Класс дескрипток порта сервера.
     Проверяет входит ли сервер в диапазон
    '''
    def __set__(self, instance, value):
        value = int(value)
        if not 1023 < value < 65536:
            # raise ValueError('Некорректный порт')
            print('Некорректный порт')
            exit(1)
        instance.__dict__[self.name] = value

    def __set_name__(self, owner, name):
        self.name = name

