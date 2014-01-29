""" setup.py
    Basic setup file to enable pip install
    See http://python-distribute.org/distribute_setup.py
    
    
    python setup.py register sdist upload 

"""

from setuptools import setup, find_packages

import saltflo

setup(
    name='saltflo',
    version=saltflo.__version__, 
    description='SaltStack interface to IoFlo',
    long_description='', 
    url='https://github.com/saltstack/saltflo',
    download_url='https://github.com/saltstack/saltflo/archive/master.zip', 
    author=saltflo.__author__,
    author_email='info@saltstack.com',
    license=saltflo.__license__,
    keywords=(''),
    packages = find_packages(exclude=['test', 'test.*',
                                      'docs', 'docs*',
                                      'log', 'log*', ]),
    package_data={
        '':       ['*.txt',  '*.md', '*.rst', '*.json', '*.conf', '*.html',
                   '*.css', '*.ico', '*.png', 'LICENSE', 'LEGAL'],
        },
    install_requires = [],
    extras_require = {},
    scripts=[],)
    
