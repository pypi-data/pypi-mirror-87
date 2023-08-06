from setuptools import setup, find_packages

setup(name="client_messager_proj",
      version="0.9.1",
      description="client_messager_proj",
      author="Vovk Vladislav",
      author_email="vovkvladyslav@yandex.ru",
      packages=find_packages(),
      install_requires=['PyQt5', 'sqlalchemy', 'Crypto']
      )
