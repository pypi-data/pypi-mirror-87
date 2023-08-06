# from distutils.core import setup
from setuptools import setup

setup(
    name='mbforbes_python_utils',
    version='0.1.1',
    author='Maxwell Forbes',
    description="Some tiny python utils so I can be lazier.",
    url="https://github.com/mbforbes/python-utils",
    license='MIT',
    py_modules=['mbforbes_python_utils'],
    long_description=open('README.md').read(),
    python_requires='>=3.6',
)
