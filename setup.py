#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import re
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

try:
    # Python2/3 compatibility
    input = raw_input
except NameError:
    pass


def get_version(*file_paths):
    """Retrieves the version from django_fine_uploader/__init__.py"""
    filename = os.path.join(os.path.dirname(__file__), *file_paths)
    version_file = open(filename).read()
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError('Unable to find version string.')


version = get_version("django_fine_uploader", "__init__.py")


if sys.argv[-1].startswith('release'):
    """
    - Let's use bumpversion, it will find the current version and change it
    based on the release type ('patch, minor or major').
    The it will commit and tag it. More info on setup.cfg.
    - Then the usual sdist | bdist_wheel upload.
    """
    try:
        import wheel
        print("Wheel version: ", wheel.__version__)
    except ImportError:
        print('Wheel library missing. Please run "pip install wheel"')
        sys.exit()

    print("Time to release!")
    options = ['patch', 'minor', 'major']
    release_type = input('Choose a release type: {}: '.format(options))
    if release_type not in options:
        print('If you are trying to publish a new release, the options are:')
        print(options)
        sys.exit(1)

    print("\nBumping version...")
    os.system('bumpversion --allow-dirty {} --config-file setup.cfg'.format(release_type))
    os.system('git tag --list')
    print("\nPush tags.")
    os.system('git push --tags')

    print("\nOkay, let's make a dist and upload it.")
    os.system('python setup.py sdist upload')
    os.system('python setup.py bdist_wheel upload')
    sys.exit()


if sys.argv[-1] == 'publish':
    try:
        import wheel
        print("Wheel version: ", wheel.__version__)
    except ImportError:
        print('Wheel library missing. Please run "pip install wheel"')
        sys.exit()
    os.system('python setup.py sdist upload')
    os.system('python setup.py bdist_wheel upload')
    sys.exit()

if sys.argv[-1] == 'tag':
    print("Tagging the version on git:")
    os.system("git tag -a %s -m 'version %s'" % (version, version))
    os.system("git push --tags")
    sys.exit()

readme = open('README.rst').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')

setup(
    name='django-fine-uploader',
    version=version,
    description="""Simple, Chunked and Concurrent uploads with Django + Fine Uploader""",
    long_description=readme + '\n\n' + history,
    author='Douglas Miranda',
    author_email='douglasmirandasilva@gmail.com',
    url='https://github.com/douglasmiranda/django-fine-uploader',
    packages=[
        'django_fine_uploader',
    ],
    include_package_data=True,
    install_requires=[],
    license="MIT",
    zip_safe=False,
    keywords='django-fine-uploader',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Framework :: Django',
        'Framework :: Django :: 1.10',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)
