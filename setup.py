from setuptools import setup
import os


README = os.path.join(os.path.dirname(__file__), 'README.md')


setup(
    name='django-simplefilters',
    version='1.0.0',
    url='https://github.com/lukaszb/django-simplefilters',
    license='MIT',
    description='Simple drop-in replacement for rest_framework.filters',
    long_description=open(README).read(),
    long_description_content_type='text/markdown',
    author='Lukasz Balcerzak',
    author_email='lukaszbalcerzak@gmail.com',
    zip_safe=False,
    py_modules=['simplefilters'],
    include_package_data=True,
    install_requires=[
        'python-dateutil',
    ],
)
