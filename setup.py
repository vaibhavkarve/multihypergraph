import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="multihypergraph",
    version="0.0.1",
    author="Vaibhav Karve",
    author_email="vaibhavskarve@gmail.com",
    description="A simple python package for graph theory that supports multi-edges, hyper-edges, looped-edges and every other combination of these.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/vaibhavkarve/multihypergraph",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
)