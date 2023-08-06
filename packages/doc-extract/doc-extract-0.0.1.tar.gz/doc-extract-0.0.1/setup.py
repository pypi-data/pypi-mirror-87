from setuptools import setup, find_packages

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="doc-extract",
    version="0.0.1",
    author="Sahar Mor",
    author_email="koryoislie@email.COM",
    description="Extract information from documents using Cloud APIs and open-source",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/saharmor/DocExtract",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)