import json
import os
from setuptools import setup, find_packages


setup(
    name='download_anime',
    version = '0.0.7',
    entry_points={'console_scripts': ["download_anime = download_anime:main"]}
)
