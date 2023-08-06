from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="UrlAutomationMachine",
    version="1.0.4",
    author="Abdulbasid Guled",
    author_email="aguled5@myseneca.ca",
    description="A CMD tool designed to check the status codes of urls",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://www.github.com/HyperTHD/URLAutomationMachine",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "urllib3 == 1.25.10",
        "colorama == 0.4.4",
        "black == 20.8b1",
        "pytest == 6.1.2",
        "argparse == 1.1",
    ],
    entry_points={"console_scripts": ["UrlAutomationMachine = src.url_checker:main"]},
    python_requires=">=3.6",
)