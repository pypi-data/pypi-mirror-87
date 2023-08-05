# Copyright 2020 Alberto Martín Mateos and Niloufar Shoeibi
# See LICENSE for details.

from setuptools import setup, find_packages
import io


def readme():
    with io.open('README.md', encoding='utf-8') as f:
        return f.read()

def requirements(filename):
    reqs = list()
    with io.open(filename, encoding='utf-8') as f:
        for line in f.readlines():
            reqs.append(line.strip())
    return reqs


setup(
    name='twinpics',
    version='0.0.206',
    packages=find_packages(),
    url="https://www.github.com/albMart/twinpics",
    download_url='https://github.com/albMart/twinpics/archive/0.0.1.tar.gz',
    license='MIT License',
    author='Alberto Martín Mateos and Niloufar Shoeibi',
    author_email='albmartinmateos@gmail.com',
    description='twinpics — Social Media Prediction Model',
    long_description=readme(),
    long_description_content_type='text/markdown',
    install_requires=requirements(filename='requirements.txt'),
    include_package_data=True,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries"
    ],
    extras_require={
        "docs": requirements(filename='docs/requirements.txt'),
        "tests": requirements(filename='tests/requirements.txt'),
    },
    python_requires='>=3',
    project_urls={
        'Bug Reports': 'https://github.com/albMart/twinpics/issues',
        'Source': 'https://github.com/albMart/twinpics',
        'Documentation': 'https://twinpics.readthedocs.io/'
    },
)