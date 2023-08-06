import setuptools

from itsimodels import __version__


with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='itsimodels',
    version=__version__,
    author='Splunk, Inc.',
    description='Model Definitions for Splunk IT Service Intelligence',
    long_description=long_description,
    long_description_content_type='text/markdown',
	url='https://github.com/splunk/itsi-models',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=2.7',
)
