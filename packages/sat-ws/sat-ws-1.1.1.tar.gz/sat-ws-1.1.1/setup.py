# -*- coding: utf-8 -*-
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="sat-ws",
    version="1.1.1",
    author="Moisés Navarro",  # TODO
    author_email="moisalejandro@gmail.com",  # TODO
    description="API to connect with SAT ws",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/HomebrewSoft/sat_ws_api",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    include_package_data=True,
    python_requires=">=3.6",
    install_requires=[
        "pyOpenSSL==19.1.0",
        "requests==2.24.0",
        "xmltodict==0.12.0",
    ],
)
