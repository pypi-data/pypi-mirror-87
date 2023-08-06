import setuptools

try:
    with open("README.md", "r") as fh:
        long_description = fh.read()
except:
    pass

setuptools.setup(
    name="RadixAPI",
    version="0.0.5.1",
    author="Guja Lomsadze",
    author_email="elguja.lomsadze.1@btu.edu.ge",
    description="Sampler/Visualizer for small Datasets",
    url="https://github.com/Lomsadze/RadixAPI",
    packages=["RadixAPI"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=["pandas", "numpy", "xlrd"],
)


# from setuptools import setup

# setup(
#     name="RadixAPI",
#     version="0.0.1",
#     description="Sampler/Visualizer for small Datasets",
#     python_requires=">=3.6",
#     py_modules=["visualize"],
#     install_requires=["pandas", "numpy", "xlrd"],
#     package_dir={"": "src"},
# )

# setup(
#     name='RadixAPI',
#     version='0.0.2',
#     author='Guja Lomsadze',
#     author_email='elguja.lomsadze.1@btu.edu.ge',
#     packages=['RadixAPI'],
#     url='http://pypi.python.org/pypi/PackageName/',
#     description="Sampler/Visualizer for small Datasets",
#     install_requires=["pandas", "numpy", "xlrd"],

# )