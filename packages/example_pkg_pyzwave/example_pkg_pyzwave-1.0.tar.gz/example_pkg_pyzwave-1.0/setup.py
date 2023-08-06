import codecs
import os
import sys
  
try:
    from setuptools import setup
except:
    from distutils.core import setup

  
def read(fname):
    
    return codecs.open(os.path.join(os.path.dirname(__file__), fname)).read()
  
  
  
NAME = "example_pkg_pyzwave"

  
PACKAGES = ["example_pkg_pyzwave",]

  
DESCRIPTION = '''this is a protocol sniffer and analysis base on z-wave'''

  
LONG_DESCRIPTION = read("README.txt")

  
KEYWORDS = "protocol analysis base on zwave"

  
AUTHOR = "chengzizzZ"

  
AUTHOR_EMAIL = "lxytls@163.com"

  
URL = "https://gitee.com/lreals/pyzwave"

  
VERSION = "1.0"

  
LICENSE = "MIT"

  
setup(
    name = NAME,
    version = VERSION,
    description = DESCRIPTION,
    long_description = LONG_DESCRIPTION,
    classifiers = [
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
    ],
    keywords = KEYWORDS,
    author = AUTHOR,
    author_email = AUTHOR_EMAIL,
    url = URL,
    license = LICENSE,
    packages = PACKAGES,
    include_package_data=True,
    zip_safe=True,
)