from setuptools import setup, find_packages

setup(name="gb_training_client",
      version="0.0.1",
      description="mess_client",
      author="Ruslan Akmanov",
      author_email="",
      packages=find_packages(),
      install_requires=['PyQt5', 'sqlalchemy', 'pycryptodome', 'pycryptodomex']
      )