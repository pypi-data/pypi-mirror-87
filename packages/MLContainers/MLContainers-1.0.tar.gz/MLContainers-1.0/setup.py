from setuptools import setup

with open("README.md","r") as fh:
  ld = fh.read()

setup(
  name = 'MLContainers',
  packages = ['MLContainers'],
  version = '1.0',
  license='License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
  description = 'Collection of Modular, Reusable ML Pipeline Components',
  long_description_content_type="text/markdown",
  author = 'Robert F. Zhang',
  author_email = 'robertzhang100@gmail.com, robertzh@wharton.upenn.edu',
  url = 'https://github.com/robertfrankzhang/MLContainers',
  download_url = 'https://github.com/robertfrankzhang/MLContainers/archive/v_1.0.tar.gz',
  keywords = ['machine learning','data analysis','data science'],
  install_requires=['numpy','pandas','scikit-learn'],
  classifiers=[
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Science/Research',
    'Topic :: Utilities',
    'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7'
  ],
  long_description=ld
)