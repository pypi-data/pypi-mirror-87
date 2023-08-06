import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="phys_const", # Replace with your own username
    version="0.0.2",
    author="Rezenter",
    author_email="nisovru@gmail.com",
    description="Pack of physical constants.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Rezenter/phys-const",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
