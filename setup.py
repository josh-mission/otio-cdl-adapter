# Copyright Contributors to the OpenTimelineIO project
#
# SPDX-License-Identifier: MIT OR Apache-2.0
#

import io
import setuptools

with io.open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setuptools.setup(
    name="otio_cdl_adapter",
    author="Joshua James Unwin",
    author_email="josh@missiondigital.co.uk",
    version="0.8",
    description="Exports a .cdl file for each clip event in an OTIO instance",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/josh-mission/otio-cdl-adapter",
    packages=setuptools.find_packages(),
    entry_points={
        "opentimelineio.plugins": "otio_cdl_adapter = otio_cdl_adapter"
    },
    package_data={
        "otio_cdl_adapter": [
            "plugin_manifest.json",
        ],
    },
    install_requires=[
        "OpenTimelineIO >= 0.12.0"
    ],
    extras_require={
        "dev": [
            "flake8",
            "pytest",
            "pytest-cov",
            "twine"
        ]
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Multimedia :: Video",
        "Topic :: Multimedia :: Video :: Display",
        "Topic :: Multimedia :: Video :: Non-Linear Editor",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English"
    ]
)
