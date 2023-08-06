import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="marshal_client",
    version="1.0.0",
    author="Michael Smith",
    author_email="michael.smith.ok@gmail.com",
    description="A python client for the Marshal job running service",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/marshaljs/python_marshal_client",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5',
)
