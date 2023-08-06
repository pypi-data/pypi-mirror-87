from setuptools import setup
import streamsx.avro
setup(
  name = 'streamsx.avro',
  packages = ['streamsx.avro'],
  include_package_data=True,
  version = streamsx.avro.__version__,
  description = 'Avro integration for IBM Streams',
  long_description = open('DESC.txt').read(),
  author = 'IBM Streams @ github.com',
  author_email = 'hegermar@de.ibm.com',
  license='Apache License - Version 2.0',
  url = 'https://github.com/IBMStreams/streamsx.avro',
  keywords = ['streams', 'ibmstreams', 'streaming', 'analytics', 'streaming-analytics', 'avro'],
  classifiers = [
    'Development Status :: 5 - Production/Stable',
    'License :: OSI Approved :: Apache Software License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
  ],
  install_requires=['streamsx>=1.14.6', 'streamsx.toolkits'],
  
  test_suite='nose.collector',
  tests_require=['nose']
)
