from setuptools import find_packages
from distutils.core import setup


# try:
#     with open('README.md') as file:
#         long_description=file.read()
# except:
#     long_description='Quantitative Finance Tools'

try:
    import pypandoc
    long_description = pypandoc.convert('README.md', 'rst')
except(IOError, ImportError):
    long_description = open('README.md').read()

setup(
    name='TradingChartz',
    version='0.1',
    description='Trading back testing and daily signal generation',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Quantsbin',
    author_email='contactus@quantsbin.com',
    url='https://github.com/quantsbin/tradingchartz',
    packages=find_packages(),
    include_package_data=True,
    license='MIT',
    classifiers=[ 'Development Status :: 3 - Alpha',
                  'Programming Language :: Python :: 3.4',
                  'Programming Language :: Python :: 3.5',
                  'Programming Language :: Python :: 3.6']
    )