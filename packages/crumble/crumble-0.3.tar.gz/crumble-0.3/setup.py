# -*- coding: utf-8 -*-
import setuptools

setuptools.setup(
    name="crumble",
    version="0.3",
    packages=setuptools.find_packages(),
	package_data={
		"": ["crumble/*","data/*"]
	},

    # metadata for upload to PyPI
    author="James Hodson",
    author_email="james.hodson@cognism.com",
    description="Cognism URL component parser. General purpose.",
    license="lGPLv3",
    keywords="cognism, machine learning, URL parsing",
    url="https://www.github.com/cognism/crumble.git",

    classifiers=[
		"Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
