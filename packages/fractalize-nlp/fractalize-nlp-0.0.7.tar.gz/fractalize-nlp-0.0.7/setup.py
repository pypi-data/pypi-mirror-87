import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="fractalize-nlp", # Replace with your own username
    version="0.0.7",
    author="Fractal Dataminds",
    author_email="gireesh@fractal-data.com",
    description="Fractalize NLP Tools",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/fractal-dataminds/fractalize_nlp",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)