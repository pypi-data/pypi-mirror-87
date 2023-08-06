import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="zware_api",
    version="0.0.25",
    author="Alfonso Brown",
    author_email="alfonso.gonzalez@casai.com",
    description="A python package to control Z-Wave devices in a ZWare network.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/casai-org/zwave_controller",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)