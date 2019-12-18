#!/usr/bin/python3

from distutils.core import setup
#from setuptools import setup
from setuptools.command.install import install
import os

class command(install):
    def run(self):
        print('Coping execution file to /usr/bin')
        os.system("cp -v bing/main.py /usr/bin/bing")
        install.run(self)

setup(
    name = "Bing Translate",
    version = "1.0",
    author = "poemdistance",
    author_email = "poemdistance@gmail.com",
    url = "",
    packages = ['bing'],
    cmdclass={'install':command}
)
