# -*- coding: utf-8 -*-
"""
This module contains the tool of sidecar.endpoint
"""
import os
from setuptools import setup, find_packages


def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

version = '0.1.0'

long_description = (
    'Change history\n'
    '**************\n'
    + '\n' +
    read('CHANGES.txt')
    + '\n' +
    'Contributors\n'
    '************\n'
    + '\n' +
    read('CONTRIBUTORS.txt')
    + '\n' +
    '')

tests_require = ['zope.testing']

setup(name='sidecar.endpoint',
      version=version,
      description="",
      long_description=long_description,
      classifiers=[
        'Programming Language :: Python :: 2.7',
        'Framework :: Plone',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License'
        ],
      keywords=('kubernetes', 'container', 'endpoint', 'discovery'),
      author='Rodrigo Montenegro de Oliveira',
      author_email='montenegro.r@gmail.com',
      url='https://github.com/rmontenegroo',
      project_urls={
	'Source': 'https://github.com/rmontenegroo/sidecar.endpoint'
      },
      license='Apache v2',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['sidecar', ],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
         'setuptools', 
         'plone.app.caching'
      ],
      tests_require=tests_require,
      extras_require=dict(tests=tests_require),
      test_suite='sidecar.endpoint.tests.test_docs.test_suite',
      entry_points="""
      # -*- entry_points -*-
      [z3c.autoinclude.plugin]
      target = plone
      """,
      setup_requires=["PasteScript"],
      paster_plugins=["ZopeSkel"],
      python_requires='>=2.7, <3',
      )
