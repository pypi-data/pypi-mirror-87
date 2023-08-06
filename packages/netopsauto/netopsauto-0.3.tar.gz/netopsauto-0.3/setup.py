from setuptools import setup, find_packages
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name = 'netopsauto',
    version = '0.3',
    packages=find_packages(),
    description='Useful tools to automate your network',
    long_description=long_description,
    long_description_content_type = 'text/markdown',
    install_requires=['junos-eznc >=2.5.4', 'bcrypt >=3.2.0', 'cryptography >=3.2.1', 'textfsm >=0.3.2'],     
    url='https://github.com/dmtx97/netopsauto',
    author='Daniel Mendez',
    author_email='dmtx97@gmail.com'
)