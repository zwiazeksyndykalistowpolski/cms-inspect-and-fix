#!/usr/bin/python3

from setuptools import setup

setup(
    name='cmsif',
    version=1.0,
    description='Malware investigation tool for CMS sites',
    long_description='Helps to compare files of a CMS site with a content from tar.gz/zip file',
    url='https://github.com/zwiazeksyndykalistowpolski/cms-inspect-and-fix',
    author='Wolnosciowiec Collective',
    author_email='admin@wolnosciowiec.org',
    maintainer='Wolnosciowiec Collective',
    maintainer_email='admin@wolnosciowiec.org',
    license='Unlicense',
    packages=[
        'cmsif_package',
        'cmsif_package.originreader'
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Topic :: Security'
    ],
    install_requires=['unittest-data-provider'],
    scripts=['bin/cmsif.py']
)
