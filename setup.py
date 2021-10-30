from setuptools import setup, find_packages

__version__ = "0.0.1"

with open("../README.md") as f:
    readme = f.read()


def get_install_reqs():
    with open("requirements.txt") as reqs_file:
        return reqs_file.read()


setup(
    name="paral",
    version=__version__,
    description="A decorator centric package to orchestrate and communicate between parallel running tasks.",
    long_description=readme,
    author="BSE Product Experience",
    author_email="claytonbez.nl@gmail.com",
    url="https://github.com/claytonbezuidenhout/paral",
    packages=find_packages(exclude=("tests", "dist")),
    install_requires=[get_install_reqs()],
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    python_requires=">=3.8",
)
