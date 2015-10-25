from setuptools import setup, find_packages
import os

version = '1.0.7'

setup(name='Products.Pakki',
      version=version,
      description="Pakki v2 dependency package",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        ],
      keywords='',
      author='Eemeli Kantola, Arttu Voutilainen, Pekka Kantola',
      author_email='eemeli.kantola@iki.fi',
      url='http://pakki2.nudata.fi/svn/pakki',
      license='BSD',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['Products'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          #'Products.ARFilePreview',
          #'Products.AROfficeTransforms',
          #'Products.CMFPlacefulWorkflow',
          'Products.DocFinderTab',
          #'Products.Ploneboard',
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
