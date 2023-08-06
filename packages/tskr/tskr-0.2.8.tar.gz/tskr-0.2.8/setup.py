
from setuptools import setup

with open("./README.md", encoding = "utf-8") as f:
    long_description = f.read()

setup(
    name = "tskr",
    version = "0.2.8",
    description = "task management tool",
    author = "team_tskr",
    author_email = "tskr.tools@gmail.com",
    url = "https://github.co.jp/",
    packages = ["tskr", "tskr.parts"],
    install_requires = ["pycrypto", "fileinit", "relpath", "sout"],
    long_description = long_description,
    long_description_content_type = "text/markdown",
    license = "CC0 v1.0",
    classifiers = [
        "Programming Language :: Python :: 3",
        "Topic :: Software Development :: Libraries",
        "License :: CC0 1.0 Universal (CC0 1.0) Public Domain Dedication"
    ],
    entry_points = """
        [console_scripts]
        tskr = tskr:tskr
    """
)
