import setuptools

import psconfig

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="psconfig-client",
    version=psconfig.VERSION,
    author=psconfig.AUTHOR,
    author_email=psconfig.AUTHOR_EMAIL,
    description="psconfig/PWA configuration parser",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/marian-babik/psconfig-client",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 2",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=2.7',
    install_requires=['requests'],
)
