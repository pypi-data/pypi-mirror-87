import os
from setuptools import find_packages, setup

current_directory = os.path.abspath(os.path.dirname(__file__))
readme = ""
if os.path.exists('README.md'):
    with open('README.md', 'r') as file:
        readme = file.read()

setup(
    name='conectividadeapp',
    version='0.0.27',
    description='Plugin de conectividade para o Netbox',
    long_description=readme,
    long_description_content_type='text/markdown',
    url='https://github.com/ufrn-netbox/conectividadeapp',
    author='Johnny, Avando, Eduardo, Rary',
    license='Apache 2.0',
    install_requires=[],
    packages=find_packages(),
    include_package_data=True,
)
