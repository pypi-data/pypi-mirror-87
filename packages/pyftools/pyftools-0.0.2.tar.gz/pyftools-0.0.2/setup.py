import setuptools

# Package meta-data.
NAME = 'pyftools'
DESCRIPTION = 'python file tools is a simple file and text processing library with batch documents.'
URL = 'https://github.com/hzcx998/pyftools'
EMAIL = '2323168280@qq.com'
AUTHOR = 'Jason Hu'
VERSION = '0.0.2'

with open("README.md", "r") as fh:
  long_description = fh.read()

setuptools.setup(
    name=NAME,
    version=VERSION,
    author=AUTHOR,
    author_email=EMAIL,
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=URL,
    packages=setuptools.find_packages(),
    license='MIT',
    classifiers=[
        # Trove classifiers
        # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy'
    ],
)