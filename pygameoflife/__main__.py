from setuptools import setup

setup(
    name='pygameoflife',
    version='1.0.0',
    description='Conway\'s Game of Life implemented with PyGame.',
    url='https://github.com/shayne-smith/Game-of-Life',
    author='Shayne Smith',
    author_email='shayne.m.smith@vanderbilt.edu',
    license='GPL-3.0',
    packages=['pygameoflife'],
    scripts=[
        'bin/pygameoflife',
        'bin/pygameoflife.bat',
    ],
    zip_safe=False,
    install_requires=[
        'pygame'
    ]
)