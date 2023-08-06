import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="DeadOrNot",
    version="0.9",
    author="Abdul Abdi",
    author_email="aabdi39@myseneca.ca",
    description="A command-line tool for reporting on the status of links in a file",
    url="https://github.com/AbdulMAbdi/deadOrNot",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "colorama",
        "requests",
        "termcolor",
        "pytest",
        "pre-commit",
        "black",
        "flake8",
        "requests-mock",
        "pytest-cov",
    ],
    packages=setuptools.find_packages(),
    entry_points={
        "console_scripts": [
            "deadOrNot = src.deadOrNot:main",
        ]
    },
    python_requires=">=3.6",
)
