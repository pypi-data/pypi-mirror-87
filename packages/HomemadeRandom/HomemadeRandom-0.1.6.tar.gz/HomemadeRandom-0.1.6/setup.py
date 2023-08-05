import setuptools
import os

def read(filename):
    return open(os.path.join(os.path.dirname(__file__), filename)).read()

setuptools.setup(
    name='HomemadeRandom',
    version='0.1.6',
    author = "Daniel Jiang",
    description = "A random number generator built from scratch for ISYE6644 class project",
    long_description=read("README.md") + '\n\n' + read("HISTORY.md"),
    long_description_content_type="text/markdown",
    license="MIT license",
    url="https://github.com/dstar30/HomemadeRandom",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
    ]
)

