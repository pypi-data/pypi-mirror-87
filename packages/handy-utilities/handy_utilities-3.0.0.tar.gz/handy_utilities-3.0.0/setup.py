

#from distutils.core import setup

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
	name = 'handy_utilities',
	version = '3.0.0',
	packages=setuptools.find_packages(),
	author = 'Ameet Chitnis',
	author_email = 'ams.chitnis@gmail.com',	
)



