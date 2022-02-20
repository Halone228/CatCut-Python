import sys
from setuptools import setup, find_packages
with open('README.md','r') as f:
    long_description = f.read()
    
version = '1.0'

deps = [
    'requests'
]

setup(
    name='CatCut Api',
    version=version,
    url='https://github.com/Halone228/CatCut-Python',
    author='Kirill Savchuk',
    author_email='randomnik192@gmail.com',
    description=('Api for site https://catcut.net'),
    license='MIT',
    python_requires='>=3.6',
    packages=find_packages(),
    install_requires=deps,
    include_package_data=True,
    long_description=long_description
)