import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="SimpleText",
    version="1.0.1",
    author="Paresh Sharma",
    author_email="paresh7903@gmail.com",
    description="A package to manage textual data in a simple fashion.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Paresh95/SimpleText",
    keywords=['Pre-processing', 'Text Analysis', 'NLP'],
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)


