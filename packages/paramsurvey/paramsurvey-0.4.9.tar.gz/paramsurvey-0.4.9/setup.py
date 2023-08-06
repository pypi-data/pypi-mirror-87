#!/usr/bin/env python

from os import path

from setuptools import setup

packages = [
    'paramsurvey',
]

test_requirements = ['pytest>=4.6', 'coverage', 'pytest-cov', 'pytest-sugar', 'coveralls', 'numpy', 'pyfakefs']
# pytest-cov requires pytest >= 4.6, dunno why this doesn't just work in travis-ci

requires = [
    'hdrhistogram',
    'pandas',
    'pandas-appender>=0.9.1',
]

extras_require = {
    'ray': ['ray>=1', 'pyarrow'],
    'mpi': ['mpi4py'],
    'test': test_requirements,  # setup no longer tests, so make them an extra that .travis.yml uses
}

setup_requires = ['setuptools_scm']

scripts = ['scripts/paramsurvey-readme-example.py']

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    description = f.read()

setup(
    name='paramsurvey',
    use_scm_version=True,
    description='A toolkit for doing parameter surveys',
    long_description=description,
    long_description_content_type='text/markdown',
    author='Greg Lindahl and others',
    author_email='lindahl@pbm.com',
    url='https://github.com/wumpus/paramsurvey',
    packages=packages,
    python_requires=">=3.5.*",
    extras_require=extras_require,
    setup_requires=setup_requires,
    install_requires=requires,
    scripts=scripts,
    license='Apache 2.0',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Operating System :: POSIX :: Linux',
        'Environment :: MacOS X',
        'Intended Audience :: Information Technology',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        #'Programming Language :: Python :: 3.5',  # ray no longer supports py3.5
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        #'Programming Language :: Python :: 3.9',  # no ray wheels for 3.9
        'Programming Language :: Python :: 3 :: Only',
    ],
)
