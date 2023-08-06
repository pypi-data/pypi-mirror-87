import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="CL_Utility_Library", # A custom Library
    version="0.1.2",
    author="carolineshewchuk",
    author_email="caroline.shewchuk@gmail.com",
    description="A custom Library",
    long_description="A custom Library",
    long_description_content_type="text/markdown",
    url="https://github.com/carolineshewchuk/RepoA/CL_Utility_Library",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)