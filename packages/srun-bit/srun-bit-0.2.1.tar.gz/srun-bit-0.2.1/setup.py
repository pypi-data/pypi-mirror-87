from setuptools import setup, find_packages

DESCRIPTION = 'A cli to login BIT (Beijing Institute of Technology) network.'
AUTHOR = 'Fang Li'
EMAIL = 'fangli-li@qq.com'
REQUIRES_PYTHON = '>=3.6.0'
URL = 'https://github.com/fangli-li/bit-srun-cli'
with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='srun-bit',
    version='0.2.1',
    packages=find_packages(),
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type="text/markdown",
    include_package_data=True,
    author=AUTHOR,
    url=URL,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'Click',
        'Requests',
    ],
    entry_points='''
        [console_scripts]
        srun-bit=cli.cli:cli
    ''',
)