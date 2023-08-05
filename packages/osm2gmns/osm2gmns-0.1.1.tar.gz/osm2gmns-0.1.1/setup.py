import setuptools

setuptools.setup(
    name='osm2gmns',
    version='0.1.1',
    author='Jiawei Lu, Xuesong Zhou',
    author_email='jiaweil9@asu.edu, xzhou74@asu.edu',
    url='https://github.com/jiawei92/OSM2GMNS',
    description='build network with gmns format using .osm file from openstreetmap',
    long_description=open('README_pypi.rst').read(),
    packages=['osm2gmns'],
    install_requires=['pandas >= 0.24.0','shapely >= 1.6']
)
