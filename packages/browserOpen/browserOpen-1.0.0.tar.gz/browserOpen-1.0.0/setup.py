import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="browserOpen", # Replace with your own username
    version="1.0.0",
    author="Prince Agrahari",
    author_email="princeagrahari2000@gmail.com",
    description="Search anything on Google Search Engine in Your Default Browser.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/PrinceMargaret/Search-in-Google.git",
    packages=setuptools.find_packages(include=("google","requests")),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)