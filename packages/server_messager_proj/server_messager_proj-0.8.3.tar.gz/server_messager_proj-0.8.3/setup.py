from setuptools import setup, find_packages

setup(name="server_messager_proj",
      version="0.8.3",
      description="server_messager_proj",
      author="Vovk Vladislav",
      author_email="vovkvladyslav@yandex.ru",
      packages=find_packages(),
      install_requires=['PyQt5', 'sqlalchemy', 'Crypto']
      )
