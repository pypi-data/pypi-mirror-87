from os import name
from setuptools import _install_setup_requires, setup, find_packages

classifiers = [
    'Development Status :: 1 - Planning',
    'Intended Audience :: Financial and Insurance Industry',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='CorpFiPy',
    version='0.0.1',
    description='A short description of the library',
    long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
    url='',
    author='Renad Gharzeddine',
    author_email='renad.gharz@outlook.com',
    license='MIT',
    classifiers=classifiers,
    keywords='finance, corporate, financial modeling, analysis',
    packages=find_packages(),
    install_setup_requires=[
        'numpy',
        'pandas',
        'matplotlib'
    ]
)