import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="vendoasg",
    version="1.0.1",
    author="Robert Lewandowski",
    author_email="r.lewandowski@asgard.gifts",
    description="Support script for Vendo API connection",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/asgard-sp-z-o-o/vendoasg",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)