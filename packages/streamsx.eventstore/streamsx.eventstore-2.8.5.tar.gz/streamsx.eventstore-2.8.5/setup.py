from setuptools import setup
import streamsx.eventstore
setup(
  name = 'streamsx.eventstore',
  packages = ['streamsx.eventstore'],
  include_package_data=True,
  version = streamsx.eventstore.__version__,
  description = 'Event Store integration for IBM Streams',
  long_description = open('DESC.txt').read(),
  author = 'IBM Streams @ github.com',
  author_email = 'hegermar@de.ibm.com',
  license='Apache License - Version 2.0',
  url = 'https://github.com/IBMStreams/streamsx.eventstore',
  keywords = ['streams', 'ibmstreams', 'streaming', 'analytics', 'streaming-analytics', 'db2', 'eventstore'],
  classifiers = [
    'Development Status :: 5 - Production/Stable',
    'License :: OSI Approved :: Apache Software License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
  ],
  install_requires=['streamsx>=1.14.6','streamsx.toolkits','streamsx.database>=1.5.0'],
  
  test_suite='nose.collector',
  tests_require=['nose']
)
