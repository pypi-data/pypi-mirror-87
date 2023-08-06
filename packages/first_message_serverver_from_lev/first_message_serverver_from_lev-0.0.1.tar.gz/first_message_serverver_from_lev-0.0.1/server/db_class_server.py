import datetime
import os

from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, ForeignKey, DateTime
from sqlalchemy.orm import mapper, sessionmaker
from sqlalchemy import default_comparator

PATH_TO_FILE = os.path.dirname(__file__)
print('----')
PATH_TO_SQL = f'sqlite:///{PATH_TO_FILE}/db_sqlite.db3'
print(PATH_TO_SQL)
print('----')


#  Класс  серверного хранилища
class ServerStorage:
    '''
    Класс хранилище
    '''

    class User:
        '''
        Класс User для хранилища данных пользователя.
        '''

        def __init__(self, username, password_hash=None):
            self.name = username
            self.register_date = datetime.datetime.now()
            self.id = None
            self.password_hash = password_hash

    # Класс обьекта Активный пользователь
    class ActiveUser:
        '''
                Класс ActiveUser для хранилища данных активности пользователя.
        '''

        def __init__(self, user_id, ip_address, port, login_time):
            self.user = user_id
            self.ip = ip_address
            self.port = port
            self.login_time = login_time

    # Класс история клиента
    class StoryClient:
        '''
                Класс для хранилища истории клиента.
        '''

        def __init__(self, name, ip_address, login_time, port):
            self.name = name
            self.date_time = login_time
            self.ip = ip_address
            self.port = port
            self.id = None

    # Класс Контакт пользователя
    class UserContact:
        '''
                Класс User для хранилища контактов пользователя.
                '''

        def __init__(self, user_id, contact_id):
            self.id = None
            self.user_id = user_id
            self.contact_id = contact_id

    def __init__(self):
        print('--- INIT --')
        self.database_engine = create_engine(PATH_TO_SQL, echo=False)
        print('Database_engine', self.database_engine)
        self.metadata = MetaData()
        # Таблица пользователь
        user_table = Table('User', self.metadata,
                           Column('id', Integer, primary_key=True),
                           Column('name', String),
                           Column('register_date', DateTime),
                           Column('password_hash', String)
                           )
        # Ктаблица активный пользователь
        active_user_table = Table('ActiveUser', self.metadata,
                                  Column('id', Integer, primary_key=True),
                                  Column('user', ForeignKey('User.id'), unique=True),
                                  Column('ip', String),
                                  Column('port', String),
                                  Column('login_time', DateTime)
                                  )
        # Таблица история пользователя
        story_table = Table('StoryTable', self.metadata,
                            Column('id', Integer, primary_key=True),
                            Column('name', ForeignKey('User.name')),
                            Column('date_time', DateTime),
                            Column('ip', String),
                            Column('port', String)
                            )
        # Таблица конатк пользователя
        user_contact_table = Table('UserContact', self.metadata,
                                   Column('id', Integer, primary_key=True),
                                   Column('user_id', ForeignKey('User.id')),
                                   Column('contact_id', ForeignKey('User.id'))
                                   )

        self.metadata.create_all(self.database_engine)

        mapper(self.User, user_table)
        mapper(self.StoryClient, story_table)
        mapper(self.ActiveUser, active_user_table)
        mapper(self.UserContact, user_contact_table)

        Session = sessionmaker(bind=self.database_engine)
        self.session = Session()
        self.session.query(self.ActiveUser).delete()
        self.session.commit()

    # Функция проверки логин - пароль Пользователя
    def user_login(self, username, ip_address, port, password_hash):
        '''
            Функция обработки входа пользователя
        '''
        print(f'Login info {username}, {ip_address}, {port}')
        rez = self.session.query(self.User).filter_by(name=username)
        print(rez)
        print('----')
        print('Rez count ', rez.count())
        print('-----')
        if rez.count():
            print('User rez count')
            print(rez.first())
            user = rez.first()
            if user.password_hash == password_hash:
                user.register_date = datetime.datetime.now()
                histroy = self.StoryClient(name=user.name, login_time=datetime.datetime.now(), ip_address=ip_address,
                                           port=port)
                new_user = self.ActiveUser(user_id=user.id, ip_address=ip_address, port=port,
                                           login_time=datetime.datetime.now())
                self.session.add(histroy)
                self.session.commit()
                return True
            else:
                return False
                print('Некорректный логин - пароль')

        else:
            print('Такого пользователя нет db_class_server')
            return False

        print('New_user_add ')

    # Функция регистрации пользовтаеля и записи его в базу
    def user_register(self, username, ip_address, port, hash_passwod):
        '''
            Функция регистрации пользователя
        '''
        print(f'Register infor {username}, {ip_address}', {port}, {hash_passwod})
        print(f'Login info {username}, {ip_address}, {port}')
        rez = self.session.query(self.User).filter_by(name=username)
        print(rez)
        print('----')
        print('Rez count ', rez.count())
        print('-----')
        if not rez.count():
            user = self.User(username, password_hash=hash_passwod)
            self.session.add(user)
            self.session.commit()
            print('REGISTER count True')
            return True
        if rez.count():
            print('Rez count FALSE', rez.count())
            return False

    # Функция logout
    def user_logout(self, username):
        '''
            Функция выхода пользователя
        '''
        user = self.session.query(self.User).filter_by(name=username).first()
        self.session.query(self.ActiveUser).filter_by(user=user.id).delete()
        self.session.commit()
        print('Delete active user')

    # Функция запроса активного пользовтаеля
    def active_user(self):
        '''
            Функция запроса активности пользователя
        '''
        query = self.session.query(
            self.User.name,
            self.ActiveUser.ip,
            self.ActiveUser.port,
            self.ActiveUser.login_time
        ).join(self.User)
        return query.all()

    # Функция запроса истории пользователя
    def login_history(self, username=None):
        '''
            Функция запроса истории входа пользователя
        '''
        query = self.session.query(self.User.name,
                                   self.StoryClient.date_time,
                                   self.StoryClient.ip,
                                   self.StoryClient.port,
                                   ).join(self.User)
        if username:
            query = query.filter(self.User.name == username)
            # query=self.session.query(self.User.name == username)
        return query.all()

    # Функция добавления контактов пользователя
    def add_contact(self, user, contact):
        '''
            Функция добавления пользователя в контакт лист
        '''
        user = self.session.query(self.User).filter_by(name=user).first()
        contact = self.session.query(self.User).filter_by(name=contact).first()

        if not contact or self.session.query(self.UserContact).filter_by(user_id=user.id,
                                                                         contact_id=contact.id).count():
            return

        contact_row = self.UserContact(user_id=user.id, contact_id=contact.id)
        self.session.add(contact_row)
        self.session.commit()

    # Фукнция удаления контактов пользовтаеля
    def remove_contact(self, user, contact):
        '''
            Функция удаления пользователя
        '''
        user = self.session.query(self.User).filter_by(name=user).first()
        contact = self.session.query(self.User).filter_by(name=contact).first()
        remove_row = self.session.query(self.UserContact).filter(
            self.UserContact.user_id == user.id, self.UserContact.contact_id == contact.id).delete()
        print('DeleteUser')
        self.session.commit()

    # Функция получения контакт листа пользовтаеля
    def contact_list(self, user):
        '''
                    Функция получения контактов сервера из базы
        '''
        user = self.session.query(self.User).filter_by(name=user).first()
        contact_list = self.session.query(self.UserContact, self.User.name). \
            filter_by(user_id=user.id). \
            join(self.User, self.UserContact.contact_id == self.User.id)

        self.session.commit()
        print(contact_list.__dict__)
        return [item[1] for item in contact_list.all()]


if __name__ == '__main__':
    print('_____MAIN_____')
    test_db = ServerStorage()
    test_db.contact_list('nik6')

    print('----')
