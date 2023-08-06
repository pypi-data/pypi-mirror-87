from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="UrlAutomationMachine",
    version="1.0.2",
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
    entry_points={"console_scripts": ["urlChecker = src.url_checker:main"]},
    python_requires=">=3.6",
)