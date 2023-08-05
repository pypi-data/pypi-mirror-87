from setuptools import setup, find_packages

setup(name="ASPER_Messenger_Server",
      version="0.11.1",
      description="messenger_server",
      author="Andrey Speransky",
      author_email="andrey.speransky@yahoo.com",
      packages=find_packages(),
      install_requires=['PyQt5', 'sqlalchemy', 'pycryptodome', 'pycryptodomex']
      )
