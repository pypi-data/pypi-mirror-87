import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="dstwrapper",
    version="0.0.3",
    author="Emil Sorensen",
    author_email="ews@intepa.dk",
    description="Python wrapper for Danmarks Statistik API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/intepa",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)