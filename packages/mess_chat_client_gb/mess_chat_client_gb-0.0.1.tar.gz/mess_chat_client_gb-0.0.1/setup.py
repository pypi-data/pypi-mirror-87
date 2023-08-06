from setuptools import setup, find_packages

setup(
      name="mess_chat_client_gb",
      version="0.0.1",
      description="mess_chat_client_gb",
      author="Pavel Stefanenko",
      author_email="p.stefanenko@gmail.com",
      packages=find_packages(),
      install_requires=['PyQt5', 'sqlalchemy', 'pycryptodome']
)
