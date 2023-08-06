import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="elephantlabs", # Replace with your own username
    version="20.12.1",
    author="Jerome Wassmuth",
    author_email="jerome.wassmuth@elephantlabs.ai",
    description="This package contains the code necessary to "
                "use and reproduce our models and projects.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://www.elephantlabs.ai",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)