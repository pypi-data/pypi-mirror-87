import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="biogl",
    version="2.1.1",
    author="Graham Larue",
    author_email="egrahamlarue@gmail.com",
    description="A collection of small bioinformatics helper functions",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/glarue/biogl",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5',
)
