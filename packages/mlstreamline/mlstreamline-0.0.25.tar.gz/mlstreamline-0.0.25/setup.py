import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mlstreamline",
    version="0.0.25",
    author="Charles Crawford",
    author_email="crawford.charles.g@gmail.com",
    description="streamlined wrapper classes for ml",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://upload.pypi.org/legacy/mlstreamline",
    packages=setuptools.find_packages(),
    py_modules=["mlstreamline"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6'
)
