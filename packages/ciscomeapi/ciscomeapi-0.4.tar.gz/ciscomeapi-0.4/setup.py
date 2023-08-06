# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open('docs/readme.rst', 'r') as readme_file:
    readme = readme_file.read()

with open('docs/history.rst', 'r') as history_file:
    history = history_file.read()

with open('requirements.txt', 'r') as f:
    requirements = f.read().splitlines()

setup_requirements = [ ]

test_requirements = [ ]

setup(
    author="Greg Anuzelli",
    author_email="anuzellig@gmail.com",
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.5',
    ],
    description="An unofficial Cisco Mobility Express Python API.",
    install_requires=[            # I get to this in a second
          'requests',
          'beautifulsoup4',
          'urllib3',
          'jinja2'
      ],
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords=['cisco', 'wireless'],
    name='ciscomeapi',
    packages=find_packages(include=['ciscomeapi']),
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/anuzellig/ciscomeapi',
    download_url='https://github.com/anuzellig/ciscomeapi/archive/v_04.tar.gz',
    version='0.4',
    zip_safe=False,
)