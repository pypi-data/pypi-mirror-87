import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyei",
    version="0.0.1",
    author="Karin Knudson",
    author_email="karink520@gmail.com",
    description="A Python package for ecological inference",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mggg/ecological-inference",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)

