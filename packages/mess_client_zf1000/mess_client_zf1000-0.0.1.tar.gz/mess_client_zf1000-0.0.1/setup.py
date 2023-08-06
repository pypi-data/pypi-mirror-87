from setuptools import setup, find_packages

setup(name="mess_client_zf1000",
      version="0.0.1",
      description="mess_client_zf1000",
      author="Nikita Shanin",
      author_email="n.shanin@mail.ru",
      packages=find_packages(),
      install_requires=['PyQt5', 'sqlalchemy', 'pycryptodome', 'pycryptodomex']
      )
