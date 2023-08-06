import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Lord_Shiva", 
    version="0.0.3",
    author="Nethran Kumarasamy",
    author_email="ramanathank18@gmail.com",
    description="IT is the demo package .",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/nethra-coding/lord_shiva",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
