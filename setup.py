from setuptools import setup, find_packages

setup(
    name='report-dh',
    version='0.9.2',
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
    description='Report Portal API',
    long_description='Report Portal API Wrapper',
    license='Apache Software License',
    author='Deyaa Hojerat',
    author_email='deyaa.hojerat.98@gmail.com',
    url='https://github.com/deyaa562/Report',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Framework :: Pytest'
    ],
    addopts='-p report'
)
