from setuptools import setup

with open("README.md", 'r') as f:
    long_description = f.read()

setup(
    name='SecureZip',
    version='0.0.1',
    description='Gathers information on a zip, mainly for seeing wether the zip could be considered malicious (Zipbomb, travelsal etc.). Work in progress.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    license='MIT',
    author='Tony Rintala',
    author_email='rintala.tony@gmail.com',
    url="https://github.com/kuviokelluja/SecureZip",
    packages=['SecureZip'],
    install_requires=['psutil'],
)