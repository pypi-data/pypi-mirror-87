import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyvimond",
    version="0.1.3",
    author="Sam Stenvall",
    author_email="sam.stenvall@nitor.com",
    description="Tiny client library for various Vimond APIs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://www.mtv.fi/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: Other/Proprietary License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
