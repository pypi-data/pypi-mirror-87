import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="busybeaver", # Replace with your own username
    version="0.0.4",
    author="Ryan Murray",
    author_email="ryanwaltermurray@gmail.com",
    description="simplify post-processing of MIKE model results into GIS formats.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/murray91/busybeaver",
    packages=setuptools.find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],
    python_requires='>=3.8',
    keywords="MIKE post-processing water modelling",
)