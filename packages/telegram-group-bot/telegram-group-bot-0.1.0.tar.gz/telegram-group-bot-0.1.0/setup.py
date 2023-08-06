import codecs
import os
import re

import setuptools


def find_version(*file_paths):
    here = os.path.abspath(os.path.dirname(__file__))
    with codecs.open(os.path.join(here, *file_paths), "r") as fp:
        version_file = fp.read()
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


setuptools.setup(
    name="telegram-group-bot",
    version=find_version("telegram_group_bot/__init__.py"),
    python_requires=">=3.9",
    packages=["telegram_group_bot"],
    install_requires=["python-telegram-bot==13.1", "pydantic==1.7.3", "click==7.1.2"],
    extras_require={
        "dev": [
            "pytest==6.1.2",
            "pytest-xdist==2.1.0",
            "pre-commit==2.9.2",
            "wheel==0.36.0",
            "twine==3.2.0",
        ],
    },
    entry_points={
        "console_scripts": ["telegram-group-bot = telegram_group_bot.cli:cli"],
    },
    include_package_data=True,
)
