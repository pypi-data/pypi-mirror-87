from setuptools import setup, find_packages

setup(name="chat_server",
      version="0.0.8",
      description="chat_server",
      author="Nikita Shumeyko",
      author_email="nikxdrummer@gmail.com",
      packages=find_packages(),
      install_requires=['PyQt5', 'sqlalchemy', 'pycryptodome', 'pycryptodomex']
      )
