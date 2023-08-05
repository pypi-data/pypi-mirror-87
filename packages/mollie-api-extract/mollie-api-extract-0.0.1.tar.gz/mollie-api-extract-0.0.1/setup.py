import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mollie-api-extract", # Replace with your own username
    version="0.0.1",
    author="Amod Kumar",
    author_email="amodk@outlook.com",
    description="Fetch data from your Mollie account",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/amodk/mollie-api-extract",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
