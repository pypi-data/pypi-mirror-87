import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="MLpkgMA",
    version="0.0.1",
    author="Marie-Ange Dahito",
    author_email="firstname.lastname@inria.fr",
    description="A small package for quality analysis of machine learning models",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/DahitoMA/Coding_challenge",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
