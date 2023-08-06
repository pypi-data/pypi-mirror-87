import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="darmok",
    version="0.0.1",
    author="gino serpa",
    author_email="gino.serpa@gmail.com",
    description="Generic data analytics library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gino-serpa/darmok.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
