import setuptools

from eventipy import __version__

version = __version__

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="eventipy",
    version=version,
    author="Jonatan Martens",
    author_email="jonatanmartenstav@gmail.com",
    description="In-memory python event library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/JonatanMartens/eventipy",
    packages=setuptools.find_packages(exclude=("tests",)),
    install_requires=[],
    exclude=["*test.py", "tests"],
    keywords="event pubsub events",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
