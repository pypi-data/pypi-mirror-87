import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mantle",
    version="0.0.1",
    author="Lenny Truong",
    author_email="lenny@cs.stanford.edu",
    description="magma standard library (version 2)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/leonardt/mantle2",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)
