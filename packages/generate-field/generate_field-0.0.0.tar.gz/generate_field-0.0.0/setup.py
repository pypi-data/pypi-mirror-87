import setuptools  # this is the "magic" import
from numpy.distutils.core import setup, Extension

lib = Extension(name='randomfield.randomq512', sources=['randomfield/randomq512.f'])
lib2 = Extension(name='randomfield.rando2asc', sources=['randomfield/rando2asc.f'])

setup(
    name='generate_field',
    packages=['randomfield'],
    ext_modules=[lib, lib2],
    entry_points={
        'console_scripts': [
            'hello = spam.cli:main',
        ],
    }
)
