from setuptools import setup, find_packages

setup(name="chat_client",
      version="0.0.8",
      description="chat_client",
      author="Nikita Shumeyko",
      author_email="nikxdrummer@gmail.com",
      packages=find_packages(),
      install_requires=['PyQt5', 'sqlalchemy', 'pycryptodome', 'pycryptodomex']
      )
