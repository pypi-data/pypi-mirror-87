import os
from setuptools import setup
with open("README.md","r") as fh:
    long_description = fh.read()
setup(
    name='easy_tk',
    version='1.0.6.1',
    license='GNU General Public License v3',
    author='Uros Mrkobrada',
    author_email='',
    description='Make Tkinter apps in an easy way using JSON.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/uros-5/easy-tk",
    packages=['easy_tk'],
    platforms='any',
    install_requires=[
        'tkintertable',
    ],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Topic :: Software Development :: User Interfaces",
        "Topic :: Utilities",
        "Topic :: Desktop Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Programming Language :: Python"
    ],
    extras_require = {
        "dev": ["pytest>=3.6",]
    },
)
