import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="nscrapy", 
    version="0.0.3",
    author="carabedo",
    author_email="carabedo@gmail.com",
    description="A small example package for scrapping argentinian newsletters",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/carabedo",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)