from setuptools import setup
import os

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name='pyaramex',
    version='0.0.2',
    author='Jordy Chetty',
    author_email='jxrrdy@gmail.com',
    url="https://github.com/zarsahq/pyaramex",
    description="A lightweight Python wrapper around Aramex web services.",
    long_description_content_type="text/markdown",
    license="MIT",
    keywords="aramex client wrapper web-service",
    long_description=read('README.md')
)

