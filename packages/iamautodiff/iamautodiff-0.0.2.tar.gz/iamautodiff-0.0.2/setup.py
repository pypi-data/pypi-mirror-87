# For PyPi Installation 

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

# To complete
setuptools.setup(
    name="iamautodiff", # Replace with your own username
    version="0.0.2",
    author="AC 207 Group 24 (Diego | Nishu | Victor | Yuxin)",
    author_email="nlahoti@mde.harvard.edu",
    description="A package for forward and reverse automatic differentiation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/AutoDiff-Dream-Team/cs107-FinalProject",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)