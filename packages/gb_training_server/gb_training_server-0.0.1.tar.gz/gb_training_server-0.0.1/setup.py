from setuptools import setup, find_packages

setup(name="gb_training_server",
      version="0.0.1",
      description="gb_training_server",
      author="Ruslan Akmanov",
      author_email="",
      packages=find_packages(),
      install_requires=['PyQt5', 'sqlalchemy', 'pycryptodome', 'pycryptodomex']
      )