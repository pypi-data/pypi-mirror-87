from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="CDA",
    version="0.1.0",
    description="College Data Analysis",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/alisoltanirad/CDA",
    author="Ali Soltani Rad",
    author_email="soltaniradali@gmail.com",
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7'
)