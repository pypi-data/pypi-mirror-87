from setuptools import setup, find_packages

setup(name="ASPER_Messenger_Client",
      version="0.11.1",
      description="Messenger_Client",
      author="Andrey Speransky",
      author_email="andrey.speransky@yahoo.com",
      packages=find_packages(),
      install_requires=['PyQt5', 'sqlalchemy', 'pycryptodome', 'pycryptodomex']
      )
