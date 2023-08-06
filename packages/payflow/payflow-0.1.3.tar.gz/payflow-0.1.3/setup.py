# -*- coding: utf-8 -*-
from setuptools import setup

pkg_vars = {}
with open('payflow/_version.py') as fp:
    exec(fp.read(), pkg_vars)

with open('README.rst') as f:
    long_description = f.read()

setup(name='payflow',
    version=pkg_vars['__version__'],
    description='Client for Flow Payment Acquirer',
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.6',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Environment :: Console',
    ],
    url='https://gitlab.com/dansanti/payflow',
    author='Daniel Santibáñez Polanco',
    author_email='dansanti@gmail.com',
    license='GPLV3+',
    packages=['payflow'],
    install_requires=['urllib3'],
    zip_safe=False)
