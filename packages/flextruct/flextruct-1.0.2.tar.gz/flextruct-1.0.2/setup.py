import os.path

#from distutils.core import setup
from setuptools import setup

version = '1.0.2'
packages = ['flextruct']


setup(name='flextruct',
      version=version,
      description='Identification of the flexible parts of a pdb described molecule (linker, double linker, terminal part or loop) given the user defined rigid bodies',
      author='Olga Roudenko',
      author_email='roudenko@synchrotron-soleil.fr',
      license='GPL >= v.3',
      platforms=['Linux', 'Windows'],
      packages=packages,
      #package_data=package_data,
      #install_requires=["numpy", "scipy"]
      )
