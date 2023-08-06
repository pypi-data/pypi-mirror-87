from setuptools import setup, find_packages

version = '2.4'

long_description = open('README.rst').read()

setup(
      name='python-cfonb',
      version=version,
      description="Pure Python lib to read/write CFONB files, forked from https://github.com/akretion/python-cfonb",
      long_description=long_description,
      classifiers=[],
      keywords=['cfonb', 'bank', 'statement', 'parser'],
      author='Dhatim',
      author_email='contact@dhatim.com',
      url='https://github.com/dhatim/python-cfonb',
      download_url = 'https://github.com/dhatim/python-cfonb/archive/2.4.tar.gz',
      license='LGPL',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      test_suite = "cfonb.tests.test_all.suite"
      )
