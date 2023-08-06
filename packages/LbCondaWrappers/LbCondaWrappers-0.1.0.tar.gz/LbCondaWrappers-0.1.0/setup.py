###############################################################################
# (c) Copyright 2020 CERN for the benefit of the LHCb Collaboration           #
#                                                                             #
# This software is distributed under the terms of the GNU General Public      #
# Licence version 3 (GPL Version 3), copied verbatim in the file "COPYING".   #
#                                                                             #
# In applying this licence, CERN does not waive the privileges and immunities #
# granted to it by virtue of its status as an Intergovernmental Organization  #
# or submit itself to any jurisdiction.                                       #
###############################################################################
from setuptools import setup, find_packages
from os.path import abspath, dirname, join
from io import open

here = abspath(dirname(__file__))

# Get the long description from the README file
with open(join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()


package_data = []

setup(
    name="LbCondaWrappers",
    use_scm_version=True,
    description="Wrappers for using LHCb CVMFS conda installations",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.cern.ch/lhcb-core/LbCondaWrappers",
    author="LHCb",
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    keywords="LHCb Core task runner",
    packages=find_packages("src"),
    package_dir={"": "src"},
    python_requires=">=3.6",
    setup_requires=["setuptools_scm"],
    install_requires=[],
    extras_require={"testing": ["pytest", "pytest-cov"]},
    package_data={"LbCondaWrappers": package_data},
    entry_points={
        "console_scripts": [
            "lb-conda=LbCondaWrappers:lb_conda",
            "lb-conda-dev=LbCondaWrappers:lb_conda_dev",
        ]
    },
    zip_safe=False,
    project_urls={
        "Bug Reports": "https://gitlab.cern.ch/lhcb-core/LbCondaWrappers/issues",
        "Source": "https://gitlab.cern.ch/lhcb-core/LbCondaWrappers",
    },
)
