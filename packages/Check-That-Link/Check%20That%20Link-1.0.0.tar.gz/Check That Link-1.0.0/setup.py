import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Check That Link",
    version="1.0.0",
    author="Tim Roberts",
    author_email="tims@email.com",
    description="Command-line tool for checking te status of links stored in a file.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/TDDR/checkThatLink",
    install_requires=[
        "argparse == 1.4.0",
        "urllib3 == 1.25.11",
        "black == 20.8b1",
        "flake8 == 3.8.4",
        "pytest == 6.1.2",
        "pytest-cov == 2.10.1",
    ],
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        "console_scripts": [
            "ctl = src.checkThatLink:main",
        ]
    },
    python_requires=">=3.6",
)
