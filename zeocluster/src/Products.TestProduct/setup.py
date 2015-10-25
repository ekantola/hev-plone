from setuptools import setup, find_packages
import sys, os

version = '0.1'

setup(name='Products.TestProduct',
      version=version,
      description="",
      long_description="""\
""",
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        ],
      keywords='',
      author='Eemeli Kantola',
      author_email='eemeli.kantola@iki.fi',
      url='',
      license='',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=True,
      install_requires=[
          'setuptools'
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
