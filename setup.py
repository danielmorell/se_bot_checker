"""
:Project: SE Bot Checker
:Contents: setup.py
:copyright: © 2020 Daniel Morell
:license: GPL-3.0, see LICENSE for more details.
:Author: Daniel Morell
"""

import io
import re
from setuptools import setup

with io.open("se_bot_checker/__init__.py", "rt", encoding="utf8") as f:
    version = re.search(r"__version__ = '(.*?)'", f.read()).group(1)

with io.open("README.md", "rt", encoding='utf8') as fh:
    readme = fh.read()

setup(
    name='se_bot_checker',
    version=version,
    license='GPLv3+',
    url='https://github.com/danielmorell/se_bot_checker',
    project_urls={
        "Source Code": "https://github.com/danielmorell/se_bot_checker",
        "Issue tracker": "https://github.com/danielmorell/se_bot_checker/issues",
    },
    author='Daniel Morell',
    author_email='office@carintek.com',
    description="This is a python library that verifies the validity of a search engine crawler.",
    long_description=readme,
    long_description_content_type="text/markdown",
    py_modules=['se_bot_checker'],
    packages=['se_bot_checker'],
    include_package_data=True,
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "Intended Audience :: Information Technology",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
)
