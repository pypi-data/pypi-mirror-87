import re
import ast
import sys

from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand


class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', "Arguments to pass to py.test")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = []

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import coverage
        import pytest

        if self.pytest_args and len(self.pytest_args) > 0:
            self.test_args.extend(self.pytest_args.strip().split(' '))
            self.test_args.append('tests/')

        cov = coverage.Coverage()
        cov.start()
        errno = pytest.main(self.test_args)
        cov.stop()
        cov.report()
        cov.html_report()
        print("Wrote coverage report to htmlcov directory")
        sys.exit(errno)


_version_re = re.compile(r'__version__\s+=\s+(.*)')

with open('rho_ml/__init__.py', 'rb') as f:
    __version__ = str(
        ast.literal_eval(
            _version_re.search(f.read().decode('utf-8')).group(1)))

setup(name='rho-ml',
      version=__version__,
      description="Standard framework for wrapping ML and other algorithms",
      long_description=open('README.md', 'r').read(),
      long_description_content_type='text/markdown',
      maintainer="Rho AI Corporation",
      license="Commercial",
      url="https://bitbucket.org/rhoai/rho-ml",
      classifiers=[
          'Intended Audience :: Developers',
          'Intended Audience :: System Administrators',
          'License :: OSI Approved :: MIT License',
          'Operating System :: OS Independent',
          'Programming Language :: Python',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.3',
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7'
      ],
      packages=find_packages(exclude=["tests"]),
      include_package_data=True,
      install_requires=[
          'attrs',
          'click>=7,<8',
      ],
      extras_require={
          'cloud': ['boto3>=1.11,<2', 'requests>=2.24.0', 'filelock>=3'],
          'docs': ['sphinx'],
          'dev': ['honcho'],
          'test': [
              'pytest', 'tox', 'coverage', 'hypothesis', 'mock>=1,<2',
              'responses>=0.10.16,<0.11', 'moto>=1.3.16,<2'
          ]
      },
      cmdclass={'test': PyTest},
      entry_points="""
        [console_scripts]
        rho_ml=rho_ml.cli.core:rho_ml
        """)
