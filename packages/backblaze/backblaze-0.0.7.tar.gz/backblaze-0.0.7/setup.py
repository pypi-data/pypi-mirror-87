import os
import re

from setuptools import setup


def get_requirements():
    with open("requirements.txt") as f:
        return f.read().splitlines()


def get_long_description():
    with open("README.md", encoding="utf8") as f:
        return f.read()


def get_variable(variable):
    with open(os.path.join("backblaze", "base.py")) as f:
        return re.search(
            "{} = ['\"]([^'\"]+)['\"]".format(variable), f.read()
        ).group(1)


setup(
    name="backblaze",
    version=get_variable("__version__"),
    url=get_variable("__url__"),
    description=get_variable("__description__"),
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    author=get_variable("__author__"),
    author_email=get_variable("__author_email__"),
    install_requires=get_requirements(),
    license=get_variable("__license__"),
    packages=[
        "backblaze",
        "backblaze.http",
        "backblaze.models",
        "backblaze.tests",
        "backblaze.tests.awaiting",
        "backblaze.tests.blocking",
        "backblaze.bucket",
        "backblaze.bucket.awaiting",
        "backblaze.bucket.blocking",
        "backblaze.key",
    ],
    python_requires=">=3.6",
    include_package_data=True,
    zip_safe=False
)
