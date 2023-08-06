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
    version='1.0.0',
    description='A powerful library meant to assist finance professionals in day-to-day tasks.',
    long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
    url='',
    author='Renad Gharzeddine',
    author_email='renad.gharz@outlook.com',
    license='MIT',
    classifiers=classifiers,
    keywords='finance, accounting, options, business, corporate, financial modeling, analysis, forecasting',
    packages=find_packages(),
    install_setup_requires=[
        'numpy',
        'pandas',
        'matplotlib',
        'missingno',
        'plotly',
        'seaborn'
    ]
)