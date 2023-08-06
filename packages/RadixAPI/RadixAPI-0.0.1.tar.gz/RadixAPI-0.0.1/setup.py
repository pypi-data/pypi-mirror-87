import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    
    name="RadixAPI",
    version="0.0.1",
    author="Guja Lomsadze",
    author_email="elguja.lomsadze.1@btu.edu.ge",
    description="Radix Sampler for small Datasets",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Lomsadze/RadixAPI",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=["pandas", "numpy", "xlrd"]
)