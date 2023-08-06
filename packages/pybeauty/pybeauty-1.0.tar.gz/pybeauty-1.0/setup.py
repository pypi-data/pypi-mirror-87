from setuptools import setup

VERSION = "v1.0"

readme = open("readme.md", "r").read();

setup(
    name = "pybeauty",
    packages = ["pybeauty"],
    version = VERSION,
    license = "MIT",
    description = "Python module for beautifully varying RGB colour sets which can be used for setting colours anywhere!",
    long_description = readme,
    long_description_content_type = "text/markdown",
    author = "Abhay Tripathi",
    author_email = "abhay.triipathi@gmail.com",
    url = "https://github.com/AbhayTr/PyBeauty",
    download_url = "https://github.com/AbhayTr/PyBeauty/archive/" + VERSION + ".tar.gz",
    keywords = ["Beauty", "RGB", "PyBeauty", "Stunning backgrounds", "colours", "varying colours"],
    classifiers = [
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
    ]
)
