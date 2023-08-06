# from setuptools import setup, find_packages

# from os import path
# this_directory = path.abspath(path.dirname(__file__))
# with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
#     long_description = f.read()
# setup(
#     name="pyProjStruct",
#     description='pyProjStruct',
#     version="0.1.5",
#     packages=find_packages(),
#     long_description=long_description,
#     long_description_content_type='text/markdown',
#     license='MIT',
# )

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyprojstruct",  # Replace with your own username
    version="0.1.1",
    author="Example Author",
    author_email="author@example.com",
    description="A small example package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
