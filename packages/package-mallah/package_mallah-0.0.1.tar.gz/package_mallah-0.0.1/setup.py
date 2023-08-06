from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]

setup(
  name='package_mallah',
  version='0.0.1',
  description='Package with two modules',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read() + '\n\n' + open('LICENCE.txt').read(),
  long_description_content_type='text/markdown',
  url='',  
  author='Mallah Cherif',
  author_email='shadowalkersw1@gmail.com',
  LICENCE='MIT', 
  classifiers=classifiers,
  keywords='modules', 
  packages=find_packages(),
  install_requires=[''] 
)