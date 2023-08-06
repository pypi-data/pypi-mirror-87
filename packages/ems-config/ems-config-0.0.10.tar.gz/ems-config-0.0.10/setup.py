from setuptools import setup
import pathlib
import os

HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

with open(HERE / "requirements.txt") as f:
    install_requires = list(f.read().splitlines())

setup(
    name='ems-config',
    author="Emil Haldrup Eriksen",
    author_email="emil.h.eriksen@gmail.com",
    description="Common configuration utilities for EMS projects",
    version=os.getenv("CI_COMMIT_TAG", "v0.0.7").strip("v"),
    url='https://gitlab.com/thedirtyfew/utilities/ems-config',
    packages=['ems_config'],
    long_description=README,
    long_description_content_type="text/markdown",
    license="MIT",
    python_requires='>=3',
    install_requires=install_requires
)
