import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="deadlinkz",
    version="1.0.1",
    author="TJ L",
    author_email="ssjarceus@outlook.com",
    description="Program that checks for dead links in a file",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/IcemanEtika/deadlinkz",
    packages=setuptools.find_packages(),
    install_requires=[
        "requests == 2.24.0",
        "colorama == 0.4.4",
        "black == 20.8b1",
        "flake8 == 3.8.4",
        "pytest == 6.1.2",
        "coverage == 5.3.0"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)