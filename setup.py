from setuptools import setup
import os


setup(
    name='django-simplefilters',
    version='0.1',
    url='https://github.com/lukaszb/django-simplefilters',
    license='MIT',
    description='Simple drop-in replacement for rest_framework.filters',
    author='Lukasz Balcerzak',
    author_email='lukaszbalcerzak@gmail.com',
    zip_safe=False,
    py_modules=['simplefilters'],
    include_package_data=True,
)
