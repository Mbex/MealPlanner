import os
from setuptools import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "MealPlanner",
    version = "0.0.1",
    author = "Mike Priestley",
    packages=['MealPlanner','setuptools','pymongo', 'Flask','flask_cors','numpy'],
    long_description=read('README.md'),
)
