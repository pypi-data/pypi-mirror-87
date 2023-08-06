from setuptools import setup, find_packages
from os.path import join, dirname

__PACKAGE__='pynvg'
__DESCRIPTION__='pynvg is a general purpose library by NVG'
__VERSION__="0.1.4"

setup(
    name=__PACKAGE__,
    version=__VERSION__,
    packages=['pynvg'],
    description=__DESCRIPTION__,
    long_description=open(join(dirname(__file__), 'README.rst')).read(),
    author="lonagi",
    install_requires=["pycryptodome==3.6.6"],
    author_email='lonagi22@gmail.com',
    url="https://github.com/lonagi/pynvg",
)