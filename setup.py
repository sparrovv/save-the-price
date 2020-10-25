from setuptools import setup

setup(
    name='krakow-domy',
    version='1.0',
    description='Collecting info about house prices through otodom',
    author='sparrovv',
    author_email='sparrovv@gmail.com',
    packages=['krakow'],
    scripts=[
        'scrape.py',
    ]
)