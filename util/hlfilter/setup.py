from setuptools import setup

setup(
    name='hlfilter',
    version='1.0',
    py_modules=['hlfilter'],
    install_requires=[
        'Click',
    ],
    entry_points='''
        [console_scripts]
        hlfilter=hlfilter:cli
    ''',
)
