from setuptools import setup, find_packages
from report._data import parse

setup(
    name='report-dh',
    version='0.10.6',
    packages=find_packages(),
    entry_points={
        'pytest11': [
            'report=report.plugin'
        ],
        'console_scripts': [
            'report-dh=report._config:config'
        ]
    },
    install_requires=[
        'requests',
        'pytest'
    ],
    setup_requires=[
        'report._data:parse'
    ],
    description='Report Portal API',
    long_description='Report Portal API Wrapper',
    license='MIT',
    author='Deyaa Hojerat',
    author_email='deyaa.hojerat.98@gmail.com',
    url='https://github.com/deyaa562/Report',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Framework :: Pytest'
    ],
    addopts='-p report'
)
