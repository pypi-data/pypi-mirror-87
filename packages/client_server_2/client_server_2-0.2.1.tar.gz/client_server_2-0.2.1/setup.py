from setuptools import setup, find_packages

setup(name="client_server_2",
      version="0.2.1",
      description="client_server_2",
      author="alex vydrin",
      author_email="alexvydrin@gb.ru",
      packages=find_packages(),
      install_requires=['PyQt5', 'sqlalchemy', 'pycryptodome']
      )
