from setuptools import setup, find_packages

setup(name="my_chat_server_nov",
      version="1.0.0",
      description="my_chat_server",
      author="Kopylov Dmitry",
      author_email="kopylovdk@gmail.com",
      packages=find_packages(),
      install_requires=['PyQt5', 'sqlalchemy', 'pycryptodome', 'pycryptodomex']
      )
