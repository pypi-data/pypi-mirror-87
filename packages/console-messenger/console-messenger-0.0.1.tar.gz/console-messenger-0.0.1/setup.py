from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name = 'console-messenger',
    version = '0.0.1',
    author="Ajay Lingayat",
    author_email="lingayatajay2810@gmail.com",
    description = "This module helps to print messages in different colours on terminal & various python IDEs using rich module.",
    url="https://github.com/Ajay2810-hub/console-messenger",
    long_description=long_description,
    long_description_content_type="text/markdown",
    py_modules = ['ConsoleMessenger'],
    package_dir = {'': 'src'},
    install_requires=[
       "rich",
    ], 
    extras_require = {
       "dev":[
       "pytest>=3.6",
       ]
    },
    classifiers=[
       "Programming Language :: Python :: 3",
       "Programming Language :: Python :: 3.5",
       "Programming Language :: Python :: 3.6",
       "Programming Language :: Python :: 3.7",
       "Programming Language :: Python :: 3.8",
       "License :: OSI Approved :: MIT License",
       "Natural Language :: English",
       "Operating System :: OS Independent",
    ],
    python_requires='>=3.0',
)
