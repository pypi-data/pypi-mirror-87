import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="multiprocessing_tools",
    version="1.0.4",
    author="Michael Smith",
    author_email="michael.smith.ok@gmail.com",
    description="Simplified Python functions for multithreaded mapping and filtering",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/smwa/multiprocessing_tools",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5',
)
