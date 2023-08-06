import os
import setuptools
from glob import glob
from os.path import basename
from os.path import dirname
from os.path import join
from os.path import splitext

here = os.path.abspath(os.path.dirname(__file__))

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="csfalcon", # Replace with your own username
    version="0.1.1",
    author="CrowdStrike",
    maintainer="Joshua Hiller",
    description="The CrowdStrike Falcon API SDK for Python 3",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/CrowdStrike/csfalcon",
    packages=setuptools.find_packages('csfalcon'),
    package_dir={'': 'csfalcon'},
    py_modules=[splitext(basename(path))[0] for path in glob('csfalcon/*.py')],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
	"requests",
	"urllib3"
    ],
    classifiers=[
        "Intended Audience :: Developers",
        "Operating System :: Unix",
        "Operating System :: POSIX",
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: The Unlicense (Unlicense)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)

