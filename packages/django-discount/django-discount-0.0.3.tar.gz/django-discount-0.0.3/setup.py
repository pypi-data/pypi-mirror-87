import os
from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.md')).read()

setup(
    name='django-discount',
    version='0.0.3',
    packages=['django_discount'],
    description='A Django App for handling creating dynamic discount system.',
    long_description=README,
    long_description_content_type='text/markdown',
    author='Execut3',
    author_email='execut3.binarycodes@gmail.com',
    url='https://github.com/Execut3/django-discount',
    license='GPT',
    install_requires=[
        'Django>=2.0'
    ],
    include_package_data=True,
)
