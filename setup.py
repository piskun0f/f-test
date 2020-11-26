import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="fishertest", # Replace with your own username
    version="0.0.13",
    author="Andrew Piskunov",
    author_email="andrepisk2000@gmail.com",
    description="A small app for calculate Fisher critery",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/piskun0f/f-test",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",        
    ],
    python_requires='>=3.6',
)