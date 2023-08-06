from setuptools import setup, find_packages

setup(name="messenger_server_gb_Aikin",
      version="0.0.1",
      description="tutorial messenger server part GB by Aikin",
      author="Aikin Yakov",
      author_email="wedel@list.ru",
      packages=find_packages(),
      install_requires=[
          'PyQt5', 
          'sqlalchemy', 
          'pycryptodome', 
          'pycryptodomex',
          ]
     )
