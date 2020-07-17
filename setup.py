from setuptools import setup

setup(
    name='krakow-domy',
    version='1.0',
    description='Collecting info about house prices in krakow',
    author='sparrovv',
    author_email='sparrovv@gmail.com',
    packages=['krakow'],  #same as name
    scripts=[
        'daily_krakow.py',
    ]
)