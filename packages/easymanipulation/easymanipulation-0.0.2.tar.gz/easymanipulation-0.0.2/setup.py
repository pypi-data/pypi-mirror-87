import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="easymanipulation", # Replace with your own username
    version="0.0.2",
    author="Scott Barnes",
    author_email="email@email.com",
    description="Utility functions for data manipulation in pandas",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/scottabarnes/Data-Scientist-Nanodegree/tree/master/2-Software-Engineering",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
