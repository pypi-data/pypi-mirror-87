import setuptools
from setuptools import setup


with open("README.md", "r") as fh:
    long_description = fh.read()

with open('VERSION') as f:
    version = f.read()

setup(
    name='securenative',
    packages=setuptools.find_packages(),
    version=version,
    license='MIT',
    description='Secure Native SDK for python',
    author='SecureNative',
    author_email='support@securenative.com',
    url='http://www.securenative.com',
    download_url='https://github.com/securenative/securenative-python/archive/0.1.tar.gz',
    keywords=["securenative", 'cyber-security'],
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=[
        "requests",
        "pycryptodome",
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)
