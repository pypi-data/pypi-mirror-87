#!/usr/bin/env python3

from setuptools import setup, find_packages

with open('README.md') as f:
    long_description = f.read()

setup(
    name='pyTSI',
    packages=find_packages(),
    version='0.3.9',
    license='MIT',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Joseba Echevarría García',
    author_email='joseba.gar@gmail.com',
    url='https://gitlab.com/josebagar/pytsi/',
    download_url='https://gitlab.com/josebagar/pytsi/-/releases/pyTSI_0.3.9',
    keywords=['Time Series Insight', 'TSI', 'TSI SDK'],
    install_requires=[
        'requests',
        'pandas'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.7',
    ],
)
