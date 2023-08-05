from setuptools import setup, find_packages

setup(name='mess_client_project',
      version='1.0.0',
      description='mess_client_project',
      author='Shalyapin Artem',
      author_email='shalyapin.artyom@yandex.ru',
      packages=find_packages(),
      install_requires=['PyQt5', 'sqlalchemy', 'pycryptodome', 'pycryptodomex'],
      )