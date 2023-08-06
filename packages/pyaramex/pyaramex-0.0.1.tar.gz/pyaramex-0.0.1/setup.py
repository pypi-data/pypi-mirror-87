from setuptools import setup
import os

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name='pyaramex',
    version='0.0.1',
    author='Jordy Chetty',
    author_email='jxrrdy@gmail.com',
    description="A lightweight Python wrapper around Aramex web services.",
    long_description_content_type="text/markdown",
    license="MIT",
    keywords="aramex client wrapper web-service",
    long_description=read('README.md')
)