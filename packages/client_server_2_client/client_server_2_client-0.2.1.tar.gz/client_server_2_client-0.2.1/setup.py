from setuptools import setup, find_packages

setup(name="client_server_2_client",
      version="0.2.1",
      description="Messenger_Client",
      author="alex vydrin",
      author_email="alexvydrin@gb.ru",
      packages=find_packages(),
      install_requires=['PyQt5', 'sqlalchemy', 'pycryptodome']
      )
