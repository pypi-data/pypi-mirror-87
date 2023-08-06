#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'requests==2.25.0',
    'Click>=7.0',
    'lxml==4.6.1',
    'tqdm==4.52.0'
]

setup_requirements = []

test_requirements = []

setup(
    author="Peter Andorfer",
    author_email='peter.andorfer@oeaw.ac.at',
    python_requires='>=3.7',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="A client to interact with freud-net API",
    entry_points={
        'console_scripts': [
            'freud_api_crawler=freud_api_crawler.cli:cli',
            'download_work=freud_api_crawler.cli:download_work',
            'flatten_files=freud_api_crawler.cli:flatten_files',
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='freud_api_crawler',
    name='freud_api_crawler',
    packages=find_packages(include=['freud_api_crawler', 'freud_api_crawler.*']),
    data_files=[
        (
            'freud_api_crawler/fixtures',
            [
                'freud_api_crawler/fixtures/tei_dummy.xml'
            ]
        ),
    ],
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/acdh-oeaw/freud_api_crawler',
    version='0.13.0',
    zip_safe=False,
)
