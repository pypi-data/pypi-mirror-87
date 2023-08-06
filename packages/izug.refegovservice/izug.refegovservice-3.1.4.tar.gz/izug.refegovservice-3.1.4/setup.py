import os
from setuptools import setup, find_packages


version = '3.1.4'
mainainter = 'Mathias Leimgruber'

tests_require = ['ftw.builder',
                 'ftw.testing',
                 'ftw.testbrowser',
                 'plone.app.testing',
                 ]

setup(name='izug.refegovservice',
      version=version,
      description="RefEgovService for izug/zug.ch",
      long_description=(open("README.rst").read() + "\n" +
                        open(os.path.join("docs", "HISTORY.txt")).read()),

      # Get more strings from
      # http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
          'Framework :: Plone',
          'Framework :: Plone :: 4.3',
          'Framework :: Plone :: 5.1',
          'Programming Language :: Python',
          'Topic :: Software Development :: Libraries :: Python Modules',
      ],

      keywords='izug refegovservice',
      author='4teamwork GmbH',
      author_email='mailto:info@4teamwork.ch',
      url='https://nourl',
      license='GPL2',

      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['izug', ],
      include_package_data=True,
      zip_safe=False,
      tests_require=tests_require,
      extras_require=dict(tests=tests_require),

      install_requires=[
          'plone.api',
          'plone.app.dexterity',
          'setuptools',
          'ftw.referencewidget',
          'ftw.upgrade',
          'ftw.table',
      ],

      entry_points="""
      # -*- Entry points: -*-
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
