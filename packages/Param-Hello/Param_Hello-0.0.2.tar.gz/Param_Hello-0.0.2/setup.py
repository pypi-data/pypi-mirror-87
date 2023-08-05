import setuptools

with open("README.md","r") as fh:
    long_description=fh.read()

setuptools.setup(
    name="Param_Hello",
    version="0.0.2",
    author="Param",
    author_email="parme542@gmail.com",
    description="Say Hello!",
    py_modules=["Param_Hello"],
    package_dir={'':'src'},
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Param542",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)