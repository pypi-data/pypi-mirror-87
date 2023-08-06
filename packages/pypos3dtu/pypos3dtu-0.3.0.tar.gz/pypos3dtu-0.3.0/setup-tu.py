# -*- coding: utf-8 -*-
'''
Created on 4 oct. 2020
Setup of Unit Tests delivery
@author: olivier
'''
import setuptools

# import pypos3d

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pypos3dtu",
    version="0.3.0",
    author="Olivier Dufailly",
    author_email="dufgrinder@laposte.net",
    description="Unit Tests for Wavefront files and Poser files manipulation library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://sourceforge.net/projects/pojamas",
    
    packages=setuptools.find_packages('tu'), # (where='tu', include=('*', )),
    package_dir={'': 'tu'},
    
    include_package_data=True,
        
    classifiers=[
        'Development Status :: 4 - Beta',
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
    ],
    install_requires=['pypos3d==0.1.6', 'numpy>=1.19', 'scipy>=1.5', 'xlrd>=1.2'],
    python_requires='>=3.6',
)
