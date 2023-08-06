from setuptools import setup
import setuptools

with open("README.md", "r") as f:
    long_description = f.read()


setup(
    name='scoutify',
    version='1.0.1',
    description='A simple Python wrapper library for Spotify WEB API',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="@fijar-lazuardy",
    author_email="fijarlaz@gmail.com",
    url='https://github.com/samsan-tech/scoutify',
    install_requires=[
        'requests>=2.20.0',
        'six>=1.10.0',
    ],
    license='LICENSE.md',
    packages=setuptools.find_packages()
)
