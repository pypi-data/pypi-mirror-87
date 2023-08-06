from setuptools import setup, find_packages

setup(name="first_message_serverver_from_lev",
      version="0.0.1",
      description="first_message_serverver_from_lev",
      author="Lev Khotylev",
      author_email="email_email@yandex.ru",
      packages=find_packages(),
      install_requires=['PyQt5', 'sqlalchemy', 'pycryptodome']
      )
