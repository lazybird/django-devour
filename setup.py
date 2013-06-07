from setuptools import setup, find_packages

import devour


setup(
    name='django-devour',
    version=devour.__version__,
    description=devour.__doc__,
    packages=find_packages(),
    url='http://github.com/lazybird/django-devour/',
    author='lazybird',
    long_description=open('README.md').read(),
    include_package_data=True,
)

