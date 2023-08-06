from io import open
from setuptools import setup, find_packages
from k50_tracker import __version__


def read(f):
    return open(f, "r", encoding='utf-8').read()


setup(
    name='k50-tracker-api',
    version=__version__,
    packages=find_packages(),
    install_requires=['requests>=2.18.2',],
    description='K50 tracker api wrapper',
    author='bzdvdn',
    author_email='bzdv.dn@gmail.com',
    url='https://github.com/bzdvdn/k50-tracker-api',
    license='MIT',
    python_requires=">=3.6",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
)
