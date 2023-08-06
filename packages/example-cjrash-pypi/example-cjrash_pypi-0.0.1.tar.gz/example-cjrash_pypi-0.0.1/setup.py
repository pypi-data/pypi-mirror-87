import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="example-cjrash_pypi", # Replace with your own username
    version="0.0.1",
    author="Jordan Rash",
    author_email="cjr@cjrash.com",
    description="Trying to learn",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jordan-rash/pythonTest",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
