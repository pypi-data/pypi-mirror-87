import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="cond",
    version="1.2.4",
    author="Nick K",
    author_email="ynkodizzy@gmail.com",
    description="Custom numeric data type for Python 3 with some additional properties",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/notTypecast/cond",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
