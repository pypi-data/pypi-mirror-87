from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='memcachedcache',
  version='0.0.1',
  description='Manage cache by using method to add data in cache, to remove data from cache, to get all keys from cache, to check memcached stats',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Himanshu Kesharwani',
  author_email='himanshu.kesharwani@protonshub.in',
  license='MIT', 
  classifiers=classifiers,
  keywords='python library', 
  packages=find_packages(),
  install_requires=[''] 
)
