
#!/usr/bin/env python

import sys
from django_frontera import __version__

try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup

readme = 'Hi'
readme_type = 'text'
with open('README.rst') as f:
    readme = f.read()
    readme_type = 'text/markdown'

install_requires = [

]

testing_extras = [
  'jinjalint>=0.5',
]

documentation_extras = [
  
]

setup(
    name='django-frontera',
    version=__version__,
    description='Utils used by Frontera.',
    author='frontera-hq',
    author_email='daniel.ortiz@nuu.co',  # For support queries, please see http://docs.wagtail.io/en/stable/support.html
    url='https://nuu.co/',
    packages=find_packages(),
    include_package_data=True,
    license='MIT',
    long_description=readme,
    long_description_content_type=readme_type,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Framework :: Django',
        'Framework :: Django :: 2.1',
        'Framework :: Django :: 2.2',
        'Framework :: Wagtail',
        'Topic :: Utilities',
    ],
    install_requires=install_requires,
    extras_require={
        'testing': testing_extras,
        'docs': documentation_extras
    },
    zip_safe=False,
)