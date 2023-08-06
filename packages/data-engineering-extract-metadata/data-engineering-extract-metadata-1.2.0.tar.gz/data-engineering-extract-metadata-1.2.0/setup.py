import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="data-engineering-extract-metadata",
    version="1.2.0",
    author="Alec Johnson",
    author_email="alec.johnson@digital.justice.gov.uk",
    description="A python package for extracting and formatting table metadata from databases",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/moj-analytical-services/data-engineering-extract-metadata/tree/v1.2.0",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires='>=3.6',
)
