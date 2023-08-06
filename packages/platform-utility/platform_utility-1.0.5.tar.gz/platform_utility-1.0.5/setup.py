import os
from setuptools import setup
from distutils.core import setup

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'Readme.rst')).read()

setup(
    name='platform_utility',
    version='1.0.5',
    packages=['utilitylibrary'],
    description='Library utility',
    long_description=README,
    author='Phattara Kiantong',
    author_email='yondaimae1429@gmail.com',
    url='https://gitlab.com/the-platform1/lib_utility',
    download_url = 'https://gitlab.com/the-platform1/lib_utility/-/archive/1.0.5/lib_utility-1.0.5.tar.gz',
    license='MIT',
)
