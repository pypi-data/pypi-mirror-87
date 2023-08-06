from setuptools import setup, find_packages

# read the contents of your README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='conpygure',
    version="0.1.0",
    license="MIT",
    packages=find_packages(exclude=('src', 'src.*', '*.src', '*.src.*')),
    author='Luca Soato',
    author_email='info@lucasoato.it',
    description='A library to con*py*gure little projects :) ',
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=['toml'],
    url="https://github.com/LucaSoato/conpygure",
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
    ]
)
