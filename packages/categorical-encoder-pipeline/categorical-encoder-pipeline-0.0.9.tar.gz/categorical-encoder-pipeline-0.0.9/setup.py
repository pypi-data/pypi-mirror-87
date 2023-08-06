import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="categorical-encoder-pipeline",
    version="0.0.9",
    author="Vicent Blanes",
    author_email="viblasel@gmail.com",
    description="Convenient categorical encoder for sklearn pipeline",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=["categorical_encoder"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
